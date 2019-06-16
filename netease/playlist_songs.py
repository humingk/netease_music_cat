# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------
import json

import pymysql

import config
from database_pool import database_pool
from netease.user_playlists import user_playlists
from netease.first_param import first_param
from netease.request_data import request_data
from logger import loggler

log = loggler()


class playlist_songs:
    """
    歌单歌曲获取类

    """

    def __init__(self):
        # 歌曲列表
        self.playlist_songs_list = []

    def get_playlist_songs_by_user_id(self, user_id=config.user_id, default_songs_max=config.default_songs_max,
                                      created_songs_max=config.created_songs_max,
                                      collected_songs_max=config.collected_songs_max,
                                      created_playlists_max=config.created_playlists_max,
                                      collected_playlists_max=config.collected_playlists_max,
                                      is_playlists_default=config.is_playlists_default,
                                      is_playlists_created=config.is_playlists_created,
                                      is_playlists_collected=config.is_playlists_collected):
        """
        通过用户id获取用户歌单列表，再获取歌单歌曲列表

        :param user_id: 用户id
        :param default_songs_max: “用户喜欢的音乐”歌单最大歌曲选取数
        :param created_songs_max: 用户创建歌单的歌曲最大选取数
        :param collected_songs_max: 用户收藏歌单的歌曲最大选取数
        :param created_playlists_max: 用户创建歌单的最大选取数
        :param collected_playlists_max: 用户收藏歌单的最大选取数
        :param is_playlists_default: 是否爬取“用户喜欢的音乐”歌单
        :param is_playlists_created: 是否爬取用户创建的歌单
        :param is_playlists_collected: 是否爬取用户收藏的歌单
        :return: status: 是否获取到歌曲
        :return: 用户歌单歌曲列表
        """
        # 获取用户的歌单列表
        content = user_playlists().get_user_playlists(user_id=user_id,
                                                      created_playlists_max=created_playlists_max,
                                                      collected_playlists_max=collected_playlists_max,
                                                      is_playlists_default=is_playlists_default,
                                                      is_playlists_created=is_playlists_created,
                                                      is_playlists_collected=is_playlists_collected)
        if content[0]:
            user_playlists_list = content[1]
        else:
            return False, []
        for playlist in user_playlists_list:
            # 获取不同类型歌单的歌曲最大数
            playlist_songs_max = config.playlist_songs_max
            playlist_type = playlist["playlist_type"]
            if playlist_type == config.default_playlist:
                playlist_songs_max = default_songs_max
            elif playlist_type == config.created_playlist:
                playlist_songs_max = created_songs_max
            elif playlist_type == config.collected_playlist:
                playlist_songs_max = collected_songs_max
            self.get_playlist_songs_by_playlist_id(playlist_id=playlist["playlist_id"],
                                                   playlist_type=playlist_type, playlist_songs_max=playlist_songs_max)

        log.debug("playlist_songs",
                  "get user-{}'s playlists-songs:songs-total-len-{}".format(user_id, len(self.playlist_songs_list)))
        return True, self.playlist_songs_list

    def get_playlist_songs_by_playlist_id(self, playlist_id=config.playlist_id, playlist_type=config.playlist_type,
                                          playlist_songs_max=config.playlist_songs_max):
        """
        获取歌单歌曲列表
        :param playlist_id: 歌单id
        :param playlist_type: 歌单类型，包括 default created collected
        :param playlist_songs_max: 歌单最大歌曲选取数
        :return: status: 是否获取到歌曲
        :return: 歌单歌曲列表
        """
        _first_param = first_param().get_first_param_playlist(playlist_id)
        content = request_data().get_request_data(first_param=_first_param[1], url=config.url_playlist)
        try:
            if content[0]:
                songs = json.loads(content[1])["playlist"]["tracks"]
            else:
                return False, []
        except Exception as e:
            log.error("get_playlist_songs failed", "playlist_id:{},error:{}".format(playlist_id, e))
            return False, []
        song_count = 0
        pool = database_pool()
        pool.execute("insert into playlist(playlist_id) values({})".format(playlist_id))
        pool.commit()
        while song_count < playlist_songs_max and song_count < len(songs):
            self.__add(songs[song_count], playlist_id, playlist_type, pool)
            song_count += 1
        pool.commit()
        log.debug("get_playlist_songs_by_playlist_id success",
                  "playlist_id:{},playlist_type:{},playlist_songs_count:{}"
                  .format(playlist_id, playlist_type, song_count))
        return True, self.playlist_songs_list

    def __add(self, song, playlist_id, playlist_type, pool):
        """
        添加歌曲

        :param song: 歌曲位移
        :param playlist_id: 歌单id
        :param playlist_type: 歌曲所属歌单类型
        :param pool: 数据库连接池
        """
        song = {
            "song_id": song["id"],
            "song_name": song["name"],
            "song_source": config.song_source_playlist,
            "song_source_type": playlist_type,
        }
        self.playlist_songs_list.append(song)
        pool.execute(
            "replace into song(song_id,song_name,song_source,song_source_type) values({},'{}',{},{})"
                .format(song["song_id"], pymysql.escape_string(song["song_name"]), song["song_source"],
                        song["song_source_type"]))
        pool.execute(
            "replace into song_playlist(song_id, playlist_id) values({},{})".format(song["song_id"], playlist_id))


if __name__ == "__main__":
    # print(playlist_songs().get_playlist_songs_by_playlist_id())
    print(playlist_songs().get_playlist_songs_by_user_id())
