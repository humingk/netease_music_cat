# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------
import time
import config
import json
from netease.first_param import first_param
from netease.request_data import request_data
from my_tools.database_tool import database_tool
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
        # 请求数据 ----------------------------------------------------
        json_data = None
        try:
            content = request_data().get_request_data(first_param=_first_param[1], url=config.url_user_rank)
            if content[0]:
                if rank_type == config.rank_type_all:
                    json_data = json.loads(content[1])["allData"]
                elif rank_type == config.rank_type_week:
                    json_data = json.loads(content[1])["weekData"]
            else:
                return False, None
        except KeyError as e:
            logger.error(
                "get_user_ranklist_songs get failed, Maybe the guy's ranklist is hidden,can you see it in the webpage ?",
                "user_id:{},rank_type:{},error_type:{},error:{}".format(user_id, rank_type, type(e), e))
            return False, None
        except Exception as e:
            logger.error("get_user_ranklist_songs get failed", "user_id:{},rank_type:{},error:{}"
                         .format(user_id, rank_type, e))
            return False, None
        # 解析数据 ----------------------------------------------------
        ranklist_id = user_id + "r" + str(rank_type)
        song_success_count = 0
        rank_list = []
        user_rank_list = []
        song_list = []
        artist_list = []
        artist_song_list = []
        song_rank_list = []
        try:
            # ranklist_id rank_type rank_date
            rank_list.append([
                ranklist_id,
                rank_type,
                int(round(time.time() * 1000))
            ])
            # user_id ranklist_id
            user_rank_list.append([
                user_id,
                ranklist_id
            ])
            while song_success_count < rank_max and song_success_count < len(json_data):
                # song_id song_name
                song_list.append([
                    json_data[song_success_count]["song"]["id"],
                    json_data[song_success_count]["song"]["name"]
                ])
                # song_id ranklist_id song_score
                song_rank_list.append([
                    json_data[song_success_count]["song"]["id"],
                    ranklist_id,
                    json_data[song_success_count]["score"]
                ])
                # artist_id artist_name artist_score
                artist_list.append([
                    json_data[song_success_count]["song"]["song"]["artist"]["id"],
                    json_data[song_success_count]["song"]["song"]["artist"]["name"],
                    json_data[song_success_count]["song"]["song"]["artist"]["score"]
                ])
                # artist_id song_id
                artist_song_list.append([
                    json_data[song_success_count]["song"]["song"]["artist"]["id"],
                    json_data[song_success_count]["song"]["id"]
                ])
                song_success_count += 1
        except Exception as e:
            logger.error("get_user_ranklist_songs parse failed",
                         "user_id:{},rank_type:{},error_type:{},song_success_count:{},error:{}".
                         format(user_id, rank_type, song_success_count, type(e), e))
            return False, None
        # 存储数据 ----------------------------------------------------
        try:
            _database_tool = database_tool()
            _database_tool.insert_many_ranklist(rank_list)
            _database_tool.insert_many_song(song_list)
            _database_tool.insert_many_artist(artist_list)
            _database_tool.commit()
            _database_tool.insert_many_user_ranklist(user_rank_list)
            _database_tool.insert_many_song_ranklist(song_rank_list)
            _database_tool.insert_many_artist_song(artist_song_list)
            _database_tool.commit()
            _database_tool.close()
        except Exception as e:
            logger.error("get_user_ranklist_songs save failed",
                         "user_id:{},rank_type:{},song_count_success,error_type:{},error:{}"
                         .format(user_id, rank_type, song_success_count, type(e), e))
            return False, None
        logger.info("get_user_ranklist_songs success",
                    "user_id:{},rank_type:{},song_success_count:{}".format(user_id, rank_type, song_success_count))
        return True, (rank_list, song_list, artist_list, user_rank_list, song_rank_list, artist_song_list)


if __name__ == "__main__":
    _database_tool = database_tool()
    _database_tool.insert_many_user([[config.user_id, config.user_name]])
    _database_tool.commit()
    _database_tool.close()
    # user_ranklist_songs().get_user_ranklist_songs(user_id=config.user_id, rank_type=config.rank_type_week)
    user_ranklist_songs().get_user_ranklist_songs(user_id=config.user_id, rank_type=config.rank_type_all)
