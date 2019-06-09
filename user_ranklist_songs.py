# !/usr/bin/env python
# -*- coding: utf-8 -*-

import config
import json
import decrypt


class user_ranklist_songs:
    """
    排行榜歌曲获取类

    """

    def __init__(self):
        # 排行榜歌曲列表
        self.user_ranklist_songs_list = []

    def get_ranklist_songs(self, user_id=config.user_id, all_rank_max=config.all_rank_max,
                           week_rank_max=config.week_rank_max):
        """
         获取排行榜歌曲列表

        :param user_id: 用户id
        :param all_rank_max: 所有排行排行榜最大数
        :param week_rank_max: 周排行排行榜最大数
        :return: 排行榜歌曲列表
        """
        json_text = json.loads(
            decrypt.get_json(user_id=user_id, url=config.url_rank, param_type="songs", total=True, offset=0,
                             proxies=""))
        json_all_data = json_text["allData"]
        json_week_data = json_text["weekData"]
        all_rank_song_count = 0
        week_rank_song_count = 0
        while all_rank_song_count < all_rank_max and all_rank_song_count < len(json_all_data):
            self.__add(all_rank_song_count, "all", json_all_data)
            all_rank_song_count += 1
        while week_rank_song_count < week_rank_max and week_rank_song_count < len(json_week_data):
            self.__add(week_rank_song_count, "week", json_week_data)
            week_rank_song_count += 1

        return self.user_ranklist_songs_list

    def __add(self, rank_song, rank_type, data):
        """
        添加到排行榜歌曲列表

        :param rank_song: 排行榜歌曲位移
        :param rank_type: 排行榜种类
        :param data: 待添加的数据
        """
        self.user_ranklist_songs_list.append({
            "rank_song_id": data[rank_song]["song"]["id"],
            "rank_song_name": data[rank_song]["song"]["name"],
            "rank_song_score": data[rank_song]["score"],
            "rank_type": rank_type
        })


if __name__ == "__main__":
    print(user_ranklist_songs().get_ranklist_songs())
