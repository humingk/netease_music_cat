# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------
import config
import sys
from my_tools.database_tool import database_tool
from netease.user_ranklist_songs import user_ranklist_songs
from netease.playlist_songs import playlist_songs
from netease.song_comments import song_comments


class user_data:
    """
    批量获取用户数据类

    热门歌单->热门歌曲->热门评论->用户
    1. 用户->听歌排行榜->歌曲(歌手)
    2. 用户->喜欢的音乐歌单,创建的歌单,收藏的歌单->歌曲(歌手)

    """

    def get_playlist_songs(self, playlist_id):
        """
        获取歌单歌曲

        :param playlist_id: 歌单id
        :return:
        """
        _database_tool = database_tool()
        _database_tool.insert_many_playlist([[playlist_id, '', 0, 0, '']])
        _database_tool.commit()
        _database_tool.close()
        playlist_songs().get_playlist_songs_by_playlist_id(playlist_id=playlist_id,
                                                           playlist_type=config.normal_playlist,
                                                           playlist_songs_max=sys.maxsize)

    def get_song_comments(self, song_start, song_count):
        """
        获取歌曲热门评论(包括用户表,歌手表)

        :param song_start: 歌曲表位移
        :param song_count: 歌曲表数目
        :return:
        """
        song_list = database_tool().select_list_limit(table="song", start=song_start, count=song_count)
        if song_list[0]:
            for song in song_list[1]:
                song_comments().get_song_comments_hot(song_id=song[0], song_comments_hot_max=1000, thread_count=10,
                                                      thread_inteval_time=2)

    def get_user_ranklists_songs(self, user_start, user_count):
        """
        多线程获取用户排行榜

        :param user_start: 用户表位移
        :param user_count: 用户表数目
        :return:
        """

        user_list = database_tool().select_list_limit(table="user", start=user_start, count=user_count)
        if user_list[0]:
            user_ranklist_songs().get_user_ranklist_songs_thread(user_list=user_list[1], thread_count=50,
                                                                 thread_inteval_time=0.1, rank_max=100)

    def get_user_playlist_songs(self, user_start, user_count):
        """
        多线程获取用户歌单

        :param user_start: 用户表位移
        :param user_count: 用户表数目
        :return:
        """
        user_list = database_tool().select_list_limit(table="user", start=user_start, count=user_count)
        if user_list[0]:
            playlist_songs().get_playlist_songs_by_user_list_thread(user_list=user_list[1], thread_count=10,
                                                                    thread_inteval_time=5, default_songs_max=200,
                                                                    created_songs_max=200,
                                                                    created_playlists_max=5,
                                                                    is_playlists_collected=False)


if __name__ == '__main__':
    u = user_data()
    # 评论过十万的歌曲歌单
    # u.get_playlist_songs(376493212)
    # 评论过五万的歌曲歌单
    # u.get_playlist_songs(455717860)
    # u.get_song_comments(song_start=0, song_count=100)
    u.get_user_ranklists_songs(user_start=5200, user_count=6000)
    # u.get_user_playlist_songs(user_start=100, user_count=200)
