# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------
import os
import sys
from my_tools.database_tool import database_tool
from surprise import evaluate, KNNBasic, Reader
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


class user_collaborative_filtering:
    """
    基于用户的协同过滤算法

    数据源 user_data

    热门歌单->热门歌曲->热门评论->用户
    1. 用户->听歌排行榜->歌曲algorithm
    2. 用户->喜欢的音乐歌单,创建的歌单,收藏的歌单->歌曲

    """

    def parse_user_song_score(self):
        """
        计算 用户-歌曲表 中的评分

        :return:
        """
        _database_tool = database_tool()
        user_song_list = _database_tool.execute(
            sql="select * from user_song where score=0", execute_type=1, return_type=2
        )
        last_user_song_list = []
        for user_song in user_song_list[1]:
            last_user_song_list.append([
                user_song[0],
                user_song[1],
                int(user_song[3] * config.factor_rank_all_score + user_song[4] * config.factor_rank_week_score +
                    user_song[5] * config.factor_playlist_like_pop + user_song[6] * config.factor_playlist_create_pop +
                    user_song[7] * config.factor_playlist_collect_pop)
            ])
        _database_tool.insert_many_user_song_column(column="score", data_list=last_user_song_list)
        _database_tool.commit()

    def get_user_song_score(self, score_min):
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
        # 设置评分标准 0-100
        reader = Reader(rating_scale=(0, 100))
        # 从pandas数据框加载数据集
        return Dataset.load_from_df(df=data_frame[["user", "song", "score"]], reader=reader)

    def model(self, algo: AlgoBase, data):
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

    def evaluate(self, algo: AlgoBase, data):
        """
        测试模型

        :param algo: 算法
        :param data: 数据集
        :return:
        """
        # cv折交叉检验
        return cross_validate(algo=algo, data=data, measures=["RMSE", "MAE"], cv=5)

    def get_neighbors(self, algo: AlgoBase, user_id, k):
        """
        获取user的近邻列表

        :param user_id:用户id
        :return:
        """
        user_id_inner = algo.trainset.to_inner_uid(user_id)
        neighbor_id_inner_list = algo.get_neighbors(iid=user_id_inner, k=k)
        neighbor_id_list = (algo.trainset.to_raw_uid(inner_id) for inner_id in neighbor_id_inner_list)
        user_neighbors = []
        _database_tool = database_tool()
        for neighbor_id in neighbor_id_list:
            user_neighbors.append(_database_tool.select_by_column(table="user", column="user_id", value=neighbor_id)[1])
        return user_neighbors


if __name__ == '__main__':
    user_cf = user_collaborative_filtering()

    # data = Dataset.load_builtin('ml-100k')
    user_cf.parse_user_song_score()
    data = user_cf.get_user_song_score(score_min=50)

    algo = user_cf.model(algo=KNNBasic(), data=data)
    print(user_cf.evaluate(algo=algo, data=data))

    user_id = config.user_id
    user_neighbors = user_cf.get_neighbors(algo=algo, user_id=user_id, k=10)
    print(user_neighbors)
