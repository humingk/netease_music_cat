# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------
import json
import config
from my_tools.database_tool import database_tool
from netease.user_playlists import user_playlists
from netease.first_param import first_param
from netease.request_data import request_data
from my_tools.logger_tool import loggler_tool

logger = loggler_tool()


class playlist_songs:
    """
    歌单歌曲获取类

    """

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
        :return: 歌单歌曲总数
        :return: 歌单歌曲列表
        """
        user_playlists_songs_list = []
        user_playlsit_songs_count = 0
        # 获取用户的歌单列表 ----------------------------------------------------
        user_playlists_list = None
        try:
            content = user_playlists().get_user_playlists(user_id=user_id,
                                                          created_playlists_max=created_playlists_max,
                                                          collected_playlists_max=collected_playlists_max,
                                                          is_playlists_default=is_playlists_default,
                                                          is_playlists_created=is_playlists_created,
                                                          is_playlists_collected=is_playlists_collected)
            if content[0]:
                user_playlists_list = content[2]
                # 获取用户的歌单歌曲列表 ----------------------------------------------------
                for playlist in user_playlists_list:
                    playlist_id = playlist[1]
                    playlist_type = playlist[2]
                    # 获取不同类型歌单的歌曲最大数
                    if playlist_type == config.default_playlist:
                        playlist_songs_max = default_songs_max
                    elif playlist_type == config.created_playlist:
                        playlist_songs_max = created_songs_max
                    elif playlist_type == config.collected_playlist:
                        playlist_songs_max = collected_songs_max
                    else:
                        return False, None
                    playlist_songs = self.get_playlist_songs_by_playlist_id(playlist_id=playlist_id,
                                                                            playlist_type=playlist_type,
                                                                            playlist_songs_max=playlist_songs_max)
                    if playlist_songs[0]:
                        user_playlsit_songs_count += playlist_songs[1]
                        user_playlists_songs_list.append(playlist_songs)
                    else:
                        return False, None
            else:
                return False, None
        except Exception as e:
            logger.error("get_playlist_songs_by_user_id failed",
                         "user_id:{},playlists_count:{},playlists_songs_count:{},error_type:{},error:{}"
                         .format(user_id, len(user_playlists_list), user_playlsit_songs_count, type(e), e))
            return False, None
        logger.info("get_playlsit_songs_by_user_id success",
                    "user_id:{}.playlists_count:{},playlists_songs_count:{}"
                    .format(user_id, len(user_playlists_list), user_playlsit_songs_count))
        return True, user_playlsit_songs_count, user_playlists_songs_list

    def get_playlist_songs_by_playlist_id(self, playlist_id=config.playlist_id, playlist_type=config.playlist_type,
                                          playlist_songs_max=config.playlist_songs_max):
        """
        通过歌单id获取歌单歌曲列表

        :param playlist_id: 歌单id
        :param playlist_type: 歌单类型，包括 default created collected
        :param playlist_songs_max: 歌单最大歌曲选取数
        :return: status: 是否获取到歌曲
        :return: 歌曲个数
        :return: 歌曲列表
        :return: 歌手列表
        :return: 歌曲歌手列表
        """
        # 请求参数 ----------------------------------------------------
        _first_param = first_param().get_first_param_playlist(playlist_id)
        # 请求数据 ----------------------------------------------------
        try:
            content = request_data().get_request_data(first_param=_first_param[1], url=config.url_playlist)
            if content[0]:
                songs_data = json.loads(content[1])["playlist"]["tracks"]
            else:
                return False, None
        except Exception as e:
            logger.error("get_playlist_songs_by_playlist_id get failed",
                         "playlist_id:{},playlist_type:{},error_type:{},error:{}"
                         .format(playlist_id, playlist_type, type(e), e))
            return False, None
        # 解析数据 ----------------------------------------------------
        song_count = 0
        song_list = []
        artist_list = []
        artist_song_list = []
        song_playlist_list = []
        try:
            while song_count < playlist_songs_max and song_count < len(songs_data):
                # song_id song_name
                song_list.append([
                    songs_data[song_count]["id"],
                    songs_data[song_count]["name"]
                ])
                # 多个歌手
                for artist in songs_data[song_count]['ar']:
                    # artist_id artist_name artist_score
                    artist_list.append([
                        artist["id"],
                        artist["name"],
                        -1
                    ])
                    # artist_id song_id
                    artist_song_list.append([
                        artist["id"],
                        songs_data[song_count]["id"]
                    ])
                # song_id playlist_id
                song_playlist_list.append([
                    songs_data[song_count]["id"],
                    playlist_id,
                    playlist_type
                ])
                song_count += 1
        except Exception as e:
            logger.error("get_playlist_songs_by_playlist_id parse failed",
                         "playlist_id:{},playlist_type:{},song_count:{},error_type:{},error:{}"
                         .format(playlist_id, playlist_type, song_count, type(e), e))
            return False, None
        # 存储数据 ----------------------------------------------------
        try:
            _database_tool = database_tool()
            _database_tool.insert_many_song(song_list)
            _database_tool.insert_many_artist(artist_list)
            _database_tool.commit()
            _database_tool.insert_many_song_playlist(song_playlist_list)
            _database_tool.insert_many_artist_song(artist_song_list)
            _database_tool.commit()
            _database_tool.close()
        except Exception as e:
            logger.error("get_playlist_songs_by_playlist_id save failed",
                         "playlist_id:{},playlist_type:{},error_type:{},error:{}"
                         .format(playlist_id, playlist_type, type(e), e))
            return False, None
        logger.info("get_playlist_songs_by_playlist_id success",
                    "playlist_id:{},playlist_type:{},song_count:{}"
                    .format(playlist_id, playlist_type, song_count))
        return True, len(song_list), song_list, artist_list, artist_song_list


if __name__ == "__main__":
    _database_tool = database_tool()
    _database_tool.insert_many_user([[config.user_id, config.user_name]])
    _database_tool.insert_many_playlist([[config.playlist_id, '', 0, 0, '']])
    _database_tool.commit()
    _database_tool.close()
    # print(playlist_songs().get_playlist_songs_by_playlist_id(config.playlist_id)[1])
    print(playlist_songs().get_playlist_songs_by_user_id(config.user_id, collected_playlists_max=100,
                                                         collected_songs_max=200)[1])
