# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------
import config
import json
import sys
from my_tools.database_tool import database_tool
from netease.first_param import first_param
from netease.request_data import request_data
from my_tools.logger_tool import loggler_tool

logger = loggler_tool()


class user_playlists:
    """
    用户歌单获取类

    """

    def get_user_playlists(self, user_id=config.user_id, created_playlists_max=config.created_playlists_max,
                           collected_playlists_max=config.collected_playlists_max,
                           is_playlists_default=config.is_playlists_default,
                           is_playlists_created=config.is_playlists_created,
                           is_playlists_collected=config.is_playlists_collected):
        """
        获取用户歌单列表
        
        :param user_id: 用户id
        :param created_playlists_max: 用户创建的歌单获取最大数
        :param collected_playlists_max: 用户收集的歌单获取最大数
        :param is_playlists_default: 是否爬取”用户喜欢的音乐“歌单
        :param is_playlists_created: 是否爬取用户创建的歌单
        :param is_playlists_collected: 是否爬取用户收藏的歌单
        :return: status: 是否获取到歌单
        :return: 歌单列表
        :return: 用户歌单列表
        """
        # 请求参数 ----------------------------------------------------
        _first_param = first_param().get_first_param_user_playlists(user_id=user_id)
        # 请求数据 ----------------------------------------------------
        try:
            content = request_data().get_request_data(_first_param[1], url=config.url_user_playlists)
            if content[0]:
                json_playlists_data = json.loads(content[1])["playlist"]
            else:
                return False, None
        except Exception as e:
            logger.error("get_user_playlists get failed",
                         "user_id:{},error_type:{},error:{}".format(user_id, type(e), e))
            return False, None
        # 解析数据 ----------------------------------------------------
        playlist_count = 0
        created_playlists_count = 0
        collected_playlists_count = 0
        playlist_list = []
        user_playlists_list = []
        try:
            while playlist_count < len(json_playlists_data):
                # ”用户喜欢的音乐“歌单
                if is_playlists_default:
                    parse = self.__parser(user_id=user_id, playlist_count=playlist_count, data=json_playlists_data,
                                          playlist_type=config.default_playlist)
                    playlist_list.append(parse["playlist_list"])
                    user_playlists_list.append(parse["user_playlist_list"])
                    playlist_count += 1
                    is_playlists_default = False
                    continue

                # 用户创建的歌单
                elif is_playlists_created:
                    # 若此处出现playlist为0的情况，说明没有爬取“用户喜欢的音乐”歌单，跳过此歌单
                    if playlist_count == 0:
                        playlist_count += 1
                        continue
                    # 是否是用户自己创建的歌单
                    elif str(json_playlists_data[playlist_count]["creator"]['userId']) == str(user_id):
                        if created_playlists_count < created_playlists_max:
                            parse = self.__parser(user_id=user_id, playlist_count=playlist_count,
                                                  data=json_playlists_data,
                                                  playlist_type=config.created_playlist)
                            playlist_list.append(parse["playlist_list"])
                            user_playlists_list.append(parse["user_playlist_list"])
                            created_playlists_count += 1
                        playlist_count += 1
                    else:
                        is_playlists_created = False
                    continue

                # 用户收藏的歌单
                elif is_playlists_collected:
                    # 是否是用户收藏的歌单
                    if str(json_playlists_data[playlist_count]["creator"]['userId']) != str(user_id):
                        if collected_playlists_count < collected_playlists_max:
                            parse = self.__parser(user_id=user_id, playlist_count=playlist_count,
                                                  data=json_playlists_data,
                                                  playlist_type=config.collected_playlist)
                            playlist_list.append(parse["playlist_list"])
                            user_playlists_list.append(parse["user_playlist_list"])
                            collected_playlists_count += 1
                    # 若此处出现不是用户收藏的歌单情况，说明用户创建歌单没有完全爬取，继续循环
                    playlist_count += 1
                    continue
                break
        except Exception as e:
            logger.error("get_user_playlists parse failed",
                         "user_id:{},created_playlists_count:{},collected_playlists_count:{},error_type:{},error:{}"
                         .format(user_id, created_playlists_count, collected_playlists_count, type(e), e))
            return False, None
        # 存储数据 ----------------------------------------------------
        try:
            _database_tool = database_tool()
            _database_tool.insert_many_playlist(playlist_list)
            _database_tool.commit()
            _database_tool.insert_many_user_playlist(user_playlists_list)
            _database_tool.commit()
            _database_tool.close()
        except Exception as e:
            logger.error("get user_playlist save failed",
                         "user_id:{},created_playlists_count:{},collected_playlists_count:{},error_type:{},error:{}"
                         .format(user_id, created_playlists_count, collected_playlists_count, type(e), e))
            return False, None
        logger.info("get user_playlist success",
                    "user_id:{},created_playlists_count:{},collected_playlists_count:{}"
                    .format(user_id, created_playlists_count, collected_playlists_count))
        return True, playlist_list, user_playlists_list

    def __parser(self, user_id, playlist_count, data, playlist_type):
        """
        解析数据

        :param user_id: 用户id
        :param playlist_count: 歌单计数器
        :param data: 待解析数据
        :param playlist_type: 歌单类型
        :return: playlist_list: 歌单列表
        :return: user_playlist_list: 用户歌单列表
        """
        return {
            "playlist_list": [
                data[playlist_count]["id"],
                data[playlist_count]["name"],
                data[playlist_count]["trackCount"],
                data[playlist_count]["playCount"],
                data[playlist_count]["updateTime"]
            ],
            "user_playlist_list": [
                user_id,
                data[playlist_count]["id"],
                playlist_type
            ]
        }


if __name__ == "__main__":
    _database_tool = database_tool()
    _database_tool.insert_many_user([[config.user_id, config.user_name]])
    _database_tool.commit()
    _database_tool.close()

    max = sys.maxsize
    # 爬取 喜欢歌单
    # print(user_playlists().get_user_playlists(config.user_id, created_playlists_max=max, collected_playlists_max=max,
    #                                           is_playlists_default=True, is_playlists_created=False,
    #                                           is_playlists_collected=False))
    # # 爬取 创建歌单
    # print(user_playlists().get_user_playlists(config.user_id, created_playlists_max=max, collected_playlists_max=max,
    #                                           is_playlists_default=False, is_playlists_created=True,
    #                                           is_playlists_collected=False))
    # print(user_playlists().get_user_playlists(config.user_id, created_playlists_max=3, collected_playlists_max=max,
    #                                           is_playlists_default=False, is_playlists_created=True,
    #                                           is_playlists_collected=False))
    # # 爬取 收藏歌单
    # print(user_playlists().get_user_playlists(config.user_id, created_playlists_max=max, collected_playlists_max=max,
    #                                           is_playlists_default=False, is_playlists_created=False,
    #                                           is_playlists_collected=True))
    # print(user_playlists().get_user_playlists(config.user_id, created_playlists_max=3, collected_playlists_max=max,
    #                                           is_playlists_default=False, is_playlists_created=False,
    #                                           is_playlists_collected=True))
    #
    # # 爬取 喜欢歌单，创建歌单
    # print(user_playlists().get_user_playlists(config.user_id, created_playlists_max=max, collected_playlists_max=max,
    #                                           is_playlists_default=True, is_playlists_created=True,
    #                                           is_playlists_collected=False))
    # print(user_playlists().get_user_playlists(config.user_id, created_playlists_max=3, collected_playlists_max=max,
    #                                           is_playlists_default=True, is_playlists_created=True,
    #                                           is_playlists_collected=False))
    # # 爬取 创建歌单，收藏歌单
    # print(user_playlists().get_user_playlists(config.user_id, created_playlists_max=max, collected_playlists_max=max,
    #                                           is_playlists_default=False, is_playlists_created=True,
    #                                           is_playlists_collected=True))
    # print(user_playlists().get_user_playlists(config.user_id, created_playlists_max=3, collected_playlists_max=4,
    #                                           is_playlists_default=False, is_playlists_created=True,
    #                                           is_playlists_collected=True))
    # # 爬取 喜欢歌单，收藏歌单
    # print(user_playlists().get_user_playlists(config.user_id, created_playlists_max=max, collected_playlists_max=max,
    #                                           is_playlists_default=True, is_playlists_created=False,
    #                                           is_playlists_collected=True))
    # print(user_playlists().get_user_playlists(config.user_id, created_playlists_max=max, collected_playlists_max=3,
    #                                           is_playlists_default=True, is_playlists_created=False,
    #                                           is_playlists_collected=True))
    #
    # # 爬取 喜欢歌单，创建歌单，收藏歌单
    print(user_playlists().get_user_playlists(config.user_id, created_playlists_max=max, collected_playlists_max=max,
                                              is_playlists_default=True, is_playlists_created=True,
                                              is_playlists_collected=True))
    # print(user_playlists().get_user_playlists(config.user_id, created_playlists_max=3, collected_playlists_max=4,
    #                                           is_playlists_default=True, is_playlists_created=True,
    #                                           is_playlists_collected=True))
