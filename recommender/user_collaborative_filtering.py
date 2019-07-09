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


class user_collaborative_filtering:
    """
    基于用户的协同过滤算法

    数据源 user_data

    热门歌单->热门歌曲->热门评论->用户
    1. 用户->听歌排行榜->歌曲
    2. 用户->喜欢的音乐歌单,创建的歌单,收藏的歌单->歌曲

    """

    def parse_user_song(self, start=0, count=sys.maxsize):
        """
        解析 用户-歌曲-评分 数据集

        :param start:起始值
        :param count:数量
        :return: DatasetAutoFolds
        """
        user_song_list = database_tool().select_list_limit(table="user_song", start=start, count=count)
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

    def model(self, algorithm: AlgoBase):
        """
        训练模型

        :param algorithm: 算法
        :return:
        """
        # 训练集合
        train_set = data.build_full_trainset()
        algorithm.fit(trainset=train_set)
        return algorithm

    def evaluate(self, algorithm: AlgoBase):
        """
        测试模型

        :param algorithm: 算法
        :return:
        """
        data = self.parse_user_song()
        # K折交叉检验
        data.split(5)
        return evaluate(algorithm, data, measures=["RMSE", "MAE"])

    def get_neighbors(self, algorithm: AlgoBase, user_id, k):
        """
        获取user的近邻列表

        :param user_id:用户id
        :return:
        """
        user_id_inner = algorithm.trainset.to_inner_uid(user_id)
        neighbor_id_inner_list = algorithm.get_neighbors(iid=user_id_inner, k=k)
        neighbor_id_list = (algorithm.trainset.to_raw_uid(inner_id) for inner_id in neighbor_id_inner_list)
        user_neighbors = []
        _database_tool = database_tool()
        for neighbor_id in neighbor_id_list:
            user_neighbors.append(_database_tool.select_by_column(table="user", column="user_id", value=neighbor_id)[1])
        return user_neighbors


if __name__ == '__main__':
    user_cf = user_collaborative_filtering()
    data = user_cf.parse_user_song()
    user_cf.evaluate(KNNBasic())

    algorithm = user_cf.model(KNNBasic())
    user_id = config.user_id
    user_neighbors = user_cf.get_neighbors(algorithm=algorithm, user_id=user_id, k=10)
    print(user_neighbors)
