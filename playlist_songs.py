# !/usr/bin/env python
# -*- coding: utf-8 -*-

import config
import bs4
import requests
from user_playlists import user_playlists


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
        :return: 用户歌单歌曲列表
        """
        # 获取用户的歌单列表
        user_playlists_list = user_playlists().get_user_playlists(user_id=user_id,
                                                                  created_playlists_max=created_playlists_max,
                                                                  collected_playlists_max=collected_playlists_max,
                                                                  is_playlists_default=is_playlists_default,
                                                                  is_playlists_created=is_playlists_created,
                                                                  is_playlists_collected=is_playlists_collected)
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

        return self.playlist_songs_list

    def get_playlist_songs_by_playlist_id(self, playlist_id=config.playlist_id, playlist_type=config.playlist_type,
                                          playlist_songs_max=config.playlist_songs_max):
        """
        获取歌单歌曲列表
        :param playlist_id: 歌单id
        :param playlist_type: 歌单类型，包括 default created collected
        :param playlist_songs_max: 歌单最大歌曲选取数
        :return: 歌单歌曲列表
        """
        response = requests.session().get(config.get_playlist_url(playlist_id), headers=config.user_headers).content
        bs = bs4.BeautifulSoup(response, "lxml")
        songs = bs.find("ul", {"class": "f-hide"})
        song_count = 0
        for song in songs.find_all("a"):
            if (song_count >= playlist_songs_max):
                break
            self.__add(song, playlist_type)
            song_count += 1
        return self.playlist_songs_list

    def __add(self, song, playlist_type):
        """
        添加歌曲

        :param song: 歌曲位移
        :param playlist_type: 歌曲所属歌单类型
        """
        # song="<a href="/song?id=1518938">As Long As You Love Me</a>"
        self.playlist_songs_list.append({
            "song_id": song["href"][9:],
            "song_name": song.get_text(),
            "song_playlist_type": playlist_type
        })


if __name__ == "__main__":
    print(playlist_songs().get_playlist_songs_by_playlist_id())
    print(playlist_songs().get_playlist_songs_by_user_id())
