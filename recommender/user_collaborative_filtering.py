# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------
import os
import sys
from my_tools.database_tool import database_tool
from surprise import evaluate, KNNBasic, Reader, dump
from surprise import SVD
from surprise import Dataset
from surprise import evaluate, print_perf
from surprise.model_selection import cross_validate
from surprise import NormalPredictor
from surprise import KNNBasic, KNNBaseline, KNNWithMeans, KNNWithZScore
import pandas
from surprise import AlgoBase
import config
import numpy
from my_tools.logger_tool import loggler_tool

logger = loggler_tool()


class user_collaborative_filtering:
    """
    基于用户的协同过滤算法

    数据源 user_data

    热门歌单->热门歌曲->热门评论->用户
    1. 用户->听歌排行榜->歌曲algorithm
    2. 用户->喜欢的音乐歌单,创建的歌单,收藏的歌单->歌曲

    """

    def parse_user_song_score(self, step=2000, end=sys.maxsize):
        """
        计算 用户-歌曲表 中的评分

        :param end:
        :param step:
        :return:
        """
        try:
            _database_tool = database_tool()
            for offset in range(0, end, step):
                user_song_list = _database_tool.execute(
                    sql="select * from user_song where score=0 limit {} offset {}".format(step, offset),
                    execute_type=1, return_type=2
                )
                if user_song_list[0] and len(user_song_list[1]) != 0:
                    last_user_song_list = []
                    for user_song in user_song_list[1]:
                        last_user_song_list.append([
                            user_song[0],
                            user_song[1],
                            int(user_song[3] * config.factor_rank_all_score + user_song[
                                4] * config.factor_rank_week_score +
                                user_song[5] * config.factor_playlist_like_pop + user_song[
                                    6] * config.factor_playlist_create_pop +
                                user_song[7] * config.factor_playlist_collect_pop)
                        ])
                    _database_tool.insert_many_user_song_column(column="score", data_list=last_user_song_list)
                    _database_tool.commit()
                    logger.debug("parse_user_song_score success", "offset:{}.step:{}".format(offset, step))
                else:
                    break
        except Exception as e:
            logger.error("parse_user_song_score fail", "error_type:{},error:{}".format(type(e), e))

    def get_user_song_score(self, score_min=50):
        """
        获取 用户-歌曲-评分 数据集

        :param score_min:数据集中最小分数
        :return: DatasetAutoFolds
        """
        user_song_list = database_tool().execute(
            sql="select user_id,song_id,score from user_song where score>{}".format(score_min),
            execute_type=1, return_type=2
        )
        # 数据集
        user_song_dict = {
            "user": [],
            "song": [],
            "score": []
        }
        if user_song_list[0]:
            for user_song in user_song_list[1]:
                user_song_dict["user"].append(user_song[0])
                user_song_dict["song"].append(user_song[1])
                user_song_dict["score"].append(user_song[2])
        # 字典转化为pandas数据框
        data_frame = pandas.DataFrame(data=user_song_dict)
        # 设置评分标准
        reader = Reader(rating_scale=(score_min, 1000))
        # 从pandas数据框加载数据集
        return Dataset.load_from_df(df=data_frame[["user", "song", "score"]], reader=reader)

    def train(self, algo: AlgoBase, data):
        """
        训练模型

        :param algo: 算法
        :param data: 数据集
        :return:
        """
        # 训练集合
        train_set = data.build_full_trainset()
        algo.fit(trainset=train_set)
        return algo

    def test(self, algo: AlgoBase, data):
        """
        测试模型

        :param algo: 算法
        :param data: 数据集
        :return:
        """
        # cv折交叉检验
        return cross_validate(algo=algo, data=data, measures=["RMSE", "MAE"], cv=5, verbose=True)

    def get_neighbors(self, algo: AlgoBase, user_id, k):
        """
        获取user的近邻列表

        :param user_id:用户id
        :return:
        """
        _database_tool = database_tool()
        # 内部id
        user_id_inner = algo.trainset.to_inner_uid(user_id)
        # 近邻内部id列表
        neighbor_id_inner_list = algo.get_neighbors(iid=user_id_inner, k=k)
        # 近邻外部id列表
        neighbor_id_list = (algo.trainset.to_raw_uid(inner_id) for inner_id in neighbor_id_inner_list)
        # 近邻用户列表
        user_neighbors = []
        for neighbor_id in neighbor_id_list:
            user_neighbors.append(_database_tool.select_by_column(table="user", column="user_id", value=neighbor_id)[1])
        return user_neighbors

    def get_neighbors_same_songs(self, user_id, user_neighbors, score_min=50, limit=200):
        """
        返回近邻列表中与user_id相同的歌曲

        :param user_id: 用户id
        :param user_neighbors: 近邻列表
        :param score_min:
        :param limit:
        :return:
        """
        _database_tool = database_tool()
        # user_id的歌曲列表
        self_song_score_list = []
        self_user_song_list = _database_tool.execute(
            sql="select * from user_song where user_id={} and score>{} order by score desc limit {}"
                .format(user_id, score_min, limit), execute_type=1, return_type=2)[1]
        for self_user_song in self_user_song_list:
            song = _database_tool.select_by_column(table="song", column="song_id", value=self_user_song[1])[1]
            # score song_id song_name
            self_song_score_list.append([
                self_user_song[2],
                song[0],
                song[1]
            ])
        # 所有近邻用户的歌曲列表
        all_user_song_score_list = []
        for user in user_neighbors:
            # 某近邻用户的歌曲列表
            user_song_score_list = []
            user_song_list = _database_tool.execute(
                sql="select * from user_song where user_id={} and score>{} order by score desc limit {}"
                    .format(user[0], score_min, limit), execute_type=1, return_type=2)[1]
            for user_song in user_song_list:
                song = _database_tool.select_by_column(table="song", column="song_id", value=user_song[1])[1]
                # score song_id song_name
                user_song_score_list.append([
                    user_song[2],
                    song[0],
                    song[1]
                ])
            # 与self相同歌曲
            same_song_score_list = [i for i in self_song_score_list if i in user_song_score_list]
            all_user_song_score_list.append({
                "user": user,
                "all": user_song_score_list,
                "same": same_song_score_list
            })

        return self_song_score_list, all_user_song_score_list

    def serialize_algo(self, algoType, score_min=50):
        """
        生成并序列化algo

        :param algoType: 算法类型对象
        :param score_min:
        :return:
        """
        try:
            # 计算score
            self.parse_user_song_score()
            # 加载数据集
            data = self.get_user_song_score(score_min=score_min)
            # 测试数据集
            self.test(algo=algoType, data=data)
            # 训练模型
            algo = self.train(algo=algoType, data=data)
            # 保存路径
            file_name = os.path.expanduser("./score" + str(score_min) + ".dump")
            # 序列化
            dump.dump(file_name=file_name, algo=algo)
        except Exception as e:
            logger.error("serialize_algo fail", "error_type:{},error:{}".format(type(e), e))

    def get_serialize_algo(self, score_min=50):
        """
        获取序列化algo

        :param score_min:
        :return:
        """
        file_name = os.path.expanduser("./score" + str(score_min) + ".dump")
        _, algo = dump.load(file_name=file_name)
        return algo


if __name__ == '__main__':
    user_cf = user_collaborative_filtering()
    user_cf.serialize_algo(algoType=KNNBasic())
    algo = user_cf.get_serialize_algo()

    user_id = config.user_id
    print("get neighbors...")
    user_neighbors = user_cf.get_neighbors(algo=algo, user_id=user_id, k=10)
    print(user_neighbors)

    print("get neighbors's same songs...")
    self_song_score_list, all_user_song_score_list = user_cf.get_neighbors_same_songs(user_id=config.user_id,
                                                                                      user_neighbors=user_neighbors)
    print(self_song_score_list)
    for user_song_score in all_user_song_score_list:
        if len(user_song_score["same"]) != 0:
            print('------------------')
            print("[" + user_song_score["user"][1] + "]")
            for same_list in user_song_score["same"]:
                print(str(same_list[0]) + " - " + same_list[2])
