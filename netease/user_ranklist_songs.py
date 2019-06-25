# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------
import time
import config
import json
from netease.first_param import first_param
from netease.request_data import request_data
from my_tools.database_pool import database_pool
from my_tools.logger_tool import loggler_tool

logger = loggler_tool()


class user_ranklist_songs:
    """
    排行榜歌曲获取类

    """

    def get_user_ranklist_songs(self, user_id=config.user_id, rank_type=config.rank_type, rank_max=config.rank_max):
        """
         获取某用户排行榜歌曲列表

        :param user_id: 用户id
        :param rank_max: 排行榜歌曲获取最大数
        :return: status: 是否获取到歌曲
        :return: 排行榜歌曲列表
        """
        # 请求参数
        _first_param = first_param().get_first_param_ranklist(user_id=user_id, rank_type=rank_type)
        # 请求数据
        content = request_data().get_request_data(first_param=_first_param[1], url=config.url_user_rank)
        try:
            if content[0]:
                if rank_type == config.rank_type_all:
                    json_data = json.loads(content[1])["allData"]
                elif rank_type == config.rank_type_week:
                    json_data = json.loads(content[1])["weekData"]
            else:
                return False, []
        except KeyError as e:
            logger.error(
                "get_user_ranklist_songs failed, Maybe the guy's ranklist is hidden,can you see it in the webpage ?",
                "user_id:{},rank_type:{},error:{}".format(user_id, rank_type, e))
            return False, []
        except Exception as e:
            logger.error("get_user_ranklist_songs failed", "user_id:{},rank_type:{},error:{}"
                         .format(user_id, rank_type, e))
            return False, []
        song_count = 0
        ranklist_id = user_id + "r" + str(rank_type)
        pool = database_pool()
        pool.insert_user(user_id=user_id)
        pool.insert_ranklist(ranklist_id=ranklist_id, ranklist_type=rank_type,
                             ranklist_date=int(round(time.time() * 1000)))
        pool.insert_user_ranklist(user_id=user_id, ranklist_id=ranklist_id)
        pool.commit()
        user_ranklist_songs = []
        while song_count < rank_max and song_count < len(json_data):
            self.__add(user_id, song_count, rank_type, ranklist_id, json_data, pool, user_ranklist_songs)
            song_count += 1
        logger.debug("get_user_ranklist_songs success", "user_id:{},rank_type:{},rank_count:{}"
                     .format(user_id, rank_type, song_count))
        pool.commit()
        return True, user_ranklist_songs

    def __add(self, user_id, song_count, rank_type, ranklist_id, json_data, pool, user_ranklist_songs):
        """
        添加到排行榜歌曲列表

        :param user_id: 用户id
        :param song_count: 排行榜歌曲位移
        :param rank_type: 排行榜种类
        :param ranklist_id: 排行榜id
        :param json_data: 待添加的数据
        :param pool: 数据库连接池
        :param user_ranklist_songs: 返回的数据
        """
        song = {
            "song_id": json_data[song_count]["song"]["id"],
            "song_name": json_data[song_count]["song"]["name"],
            "song_score": json_data[song_count]["score"]
        }
        artist = {
            "artist_id": json_data[song_count]["song"]["song"]["artist"]["id"],
            "artist_name": json_data[song_count]["song"]["song"]["artist"]["name"],
            "artist_score": json_data[song_count]["song"]["song"]["artist"]["score"]
        }
        user_ranklist_songs.append({"song": song, "artist": artist})
        pool.insert_song(song_id=song["song_id"], song_name=song["song_name"])
        pool.insert_artist(artist_id=artist["artist_id"], artist_name=artist["artist_name"],
                           artist_score=artist["artist_score"])
        pool.insert_song_ranklist(song_id=song["song_id"], ranklist_id=ranklist_id, song_score=song["song_score"])
        pool.insert_artist_song(artist_id=artist["artist_id"], song_id=song["song_id"])


if __name__ == "__main__":
    # print(user_ranklist_songs().get_user_ranklist_songs(user_id=config.user_id, rank_type=config.rank_type_week))
    print(user_ranklist_songs().get_user_ranklist_songs(user_id=config.user_id, rank_type=config.rank_type_all))
