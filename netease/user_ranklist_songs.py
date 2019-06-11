# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------
import config
import json
from netease.decrypt import decrypt
import logger

log = logger.loggler()


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
        :return: status: 是否获取到歌曲
        :return: 排行榜歌曲列表
        """
        context = decrypt().get_json(user_id=user_id, url=config.url_rank, param_type="songs", total=True, offset=0,
                                     proxies="")
        if context[0]:
            json_text = json.loads(context[1])
        else:
            return False, []
        json_all_data = json_text["allData"]
        json_week_data = json_text["weekData"]
        all_rank_song_count = 0
        week_rank_song_count = 0
        while all_rank_song_count < all_rank_max and all_rank_song_count < len(json_all_data):
            self.__add(all_rank_song_count, "all", json_all_data, config.rank_song_source)
            all_rank_song_count += 1
        while week_rank_song_count < week_rank_max and week_rank_song_count < len(json_week_data):
            self.__add(week_rank_song_count, "week", json_week_data, config.rank_song_source)
            week_rank_song_count += 1

        log.debug("get_ranklist_songs",
                  "get user-{}'s ranklist_songs total-len:{}".format(user_id, len(self.user_ranklist_songs_list)))
        return True, self.user_ranklist_songs_list

    def __add(self, rank_song, rank_type, data, song_source_type=config.song_source_type):
        """
        添加到排行榜歌曲列表

        :param rank_song: 排行榜歌曲位移
        :param rank_type: 排行榜种类
        :param data: 待添加的数据
        """
        self.user_ranklist_songs_list.append({
            "song_id": data[rank_song]["song"]["id"],
            "song_name": data[rank_song]["song"]["name"],
            "song_source_type": song_source_type,
            "song_source_rank_type": rank_type,
            "rank_song_score": data[rank_song]["score"]
        })


if __name__ == "__main__":
    print(user_ranklist_songs().get_ranklist_songs())
