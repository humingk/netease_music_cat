# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------
import config
import json
import sys
from netease.first_param import first_param
from netease.request_data import request_data
import logger

log = logger.loggler()


class user_playlists:
    """
    用户歌单获取类

    """

    def __init__(self):
        # 用户歌单的id列表
        self.user_playlists_list = []

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
        """
        # 请求参数
        _first_param = first_param().get_first_param_user_playlists(user_id=user_id)
        content = request_data().get_request_data(_first_param[1], url=config.url_user_playlists)
        if content[0]:
            json_playlists_data = json.loads(content[1])["playlist"]
        else:
            return False, []
        playlist_count = 0
        created_playlists_count = 0
        collected_playlists_count = 0
        while playlist_count < len(json_playlists_data):

            # 爬取”用户喜欢的音乐“这一个歌单
            if is_playlists_default:
                self.__add(playlist_count=playlist_count, data=json_playlists_data,
                           playlist_type=config.default_playlist)
                playlist_count += 1
                is_playlists_default = False
                continue

            # 爬取用户创建的歌单
            elif is_playlists_created:
                # 若此处出现playlist为0的情况，说明没有爬取“用户喜欢的音乐”歌单，跳过此歌单
                if playlist_count == 0:
                    playlist_count += 1
                    continue
                # 是否是用户自己创建的歌单
                elif str(json_playlists_data[playlist_count]["creator"]['userId']) == str(user_id):
                    if created_playlists_count < created_playlists_max:
                        self.__add(playlist_count=playlist_count, data=json_playlists_data,
                                   playlist_type=config.created_playlist)
                        created_playlists_count += 1
                    playlist_count += 1
                else:
                    is_playlists_created = False
                continue

            # 爬取用户收藏的歌单
            elif is_playlists_collected:
                # 是否是用户收藏的歌单
                if str(json_playlists_data[playlist_count]["creator"]['userId']) != str(user_id):
                    if collected_playlists_count < collected_playlists_max:
                        self.__add(playlist_count=playlist_count, data=json_playlists_data,
                                   playlist_type=config.collected_playlist)
                        collected_playlists_count += 1
                # 若此处出现不是用户收藏的歌单情况，说明用户创建歌单没有完全爬取，继续循环
                playlist_count += 1
                continue
            break

        log.debug("get user_playlists success",
                  "user_id:{},playlist_sum:{},playlist_created_sum:{},playlist_collected_sum:{}"
                  .format(user_id, playlist_count, created_playlists_count, collected_playlists_count))
        return True, self.user_playlists_list

    def __add(self, playlist_count, data, playlist_type=config.playlist_type):
        """
        添加到用户歌单列表

        :param playlist_count: 歌单列表位移
        :param data: 待添加数据
        :param playlist_type: 歌单类型
        """
        self.user_playlists_list.append({
            "playlist_id": data[playlist_count]["id"],
            "playlist_name": data[playlist_count]["name"],
            "playlist_type": playlist_type,
            "playlist_playCount": data[playlist_count]["playCount"]
        })


if __name__ == "__main__":
    max = sys.maxsize
    # 爬取 喜欢歌单
    print(user_playlists().get_user_playlists(config.user_id, created_playlists_max=max, collected_playlists_max=max,
                                              is_playlists_default=True, is_playlists_created=False,
                                              is_playlists_collected=False))
    # 爬取 创建歌单
    print(user_playlists().get_user_playlists(config.user_id, created_playlists_max=max, collected_playlists_max=max,
                                              is_playlists_default=False, is_playlists_created=True,
                                              is_playlists_collected=False))
    print(user_playlists().get_user_playlists(config.user_id, created_playlists_max=3, collected_playlists_max=max,
                                              is_playlists_default=False, is_playlists_created=True,
                                              is_playlists_collected=False))
    # 爬取 收藏歌单
    print(user_playlists().get_user_playlists(config.user_id, created_playlists_max=max, collected_playlists_max=max,
                                              is_playlists_default=False, is_playlists_created=False,
                                              is_playlists_collected=True))
    print(user_playlists().get_user_playlists(config.user_id, created_playlists_max=3, collected_playlists_max=max,
                                              is_playlists_default=False, is_playlists_created=False,
                                              is_playlists_collected=True))

    # 爬取 喜欢歌单，创建歌单
    print(user_playlists().get_user_playlists(config.user_id, created_playlists_max=max, collected_playlists_max=max,
                                              is_playlists_default=True, is_playlists_created=True,
                                              is_playlists_collected=False))
    print(user_playlists().get_user_playlists(config.user_id, created_playlists_max=3, collected_playlists_max=max,
                                              is_playlists_default=True, is_playlists_created=True,
                                              is_playlists_collected=False))
    # 爬取 创建歌单，收藏歌单
    print(user_playlists().get_user_playlists(config.user_id, created_playlists_max=max, collected_playlists_max=max,
                                              is_playlists_default=False, is_playlists_created=True,
                                              is_playlists_collected=True))
    print(user_playlists().get_user_playlists(config.user_id, created_playlists_max=3, collected_playlists_max=4,
                                              is_playlists_default=False, is_playlists_created=True,
                                              is_playlists_collected=True))
    # 爬取 喜欢歌单，收藏歌单
    print(user_playlists().get_user_playlists(config.user_id, created_playlists_max=max, collected_playlists_max=max,
                                              is_playlists_default=True, is_playlists_created=False,
                                              is_playlists_collected=True))
    print(user_playlists().get_user_playlists(config.user_id, created_playlists_max=max, collected_playlists_max=3,
                                              is_playlists_default=True, is_playlists_created=False,
                                              is_playlists_collected=True))

    # 爬取 喜欢歌单，创建歌单，收藏歌单
    print(user_playlists().get_user_playlists(config.user_id, created_playlists_max=max, collected_playlists_max=max,
                                              is_playlists_default=True, is_playlists_created=True,
                                              is_playlists_collected=True))
    print(user_playlists().get_user_playlists(config.user_id, created_playlists_max=3, collected_playlists_max=4,
                                              is_playlists_default=True, is_playlists_created=True,
                                              is_playlists_collected=True))