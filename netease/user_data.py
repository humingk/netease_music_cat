# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------
import time
from concurrent.futures import ThreadPoolExecutor

import config
import sys
from my_tools.database_tool import database_tool
from netease.user_ranklist_songs import user_ranklist_songs
from netease.playlist_songs import playlist_songs
from netease.song_comments import song_comments
from my_tools.logger_tool import loggler_tool

logger = loggler_tool()


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

    def get_user_songs(self, user_start, user_count, thread_count=20, thread_inteval_time=5):
        """
        多线程获取用户 排行榜+歌单

        :param user_start: 用户表位移
        :param user_count: 用户表数目
        :param thread_count: 线程数
        :param thread_inteval_time: 线程间隔时间
        :return:
        """
        user_list = database_tool().select_list_limit(table="user", start=user_start, count=user_count)[1]
        try:
            success_count = 0
            _user_ranklist_songs = user_ranklist_songs()
            _playlist_songs = playlist_songs()
            with ThreadPoolExecutor(thread_count) as executer:
                future_list = []
                for user in user_list:
                    future_rank_all = executer.submit(_user_ranklist_songs.get_user_ranklist_songs,
                                                      user[0], config.rank_type_all, config.all_rank_max)
                    future_rank_week = executer.submit(_user_ranklist_songs.get_user_ranklist_songs,
                                                       user[0], config.rank_type_week, config.week_rank_max)
                    future_playlist = executer.submit(_playlist_songs.get_playlist_songs_by_user_id, user[0])
                    future_list.append(future_rank_all)
                    future_list.append(future_rank_week)
                    future_list.append(future_playlist)
                    time.sleep(thread_inteval_time)
                for future in future_list:
                    if future.result()[0]:
                        success_count += 1
            return True
        except Exception as e:
            logger.error("get_user_songs failed", "error_type:{},error:{}"
                         .format(type(e), e))


if __name__ == '__main__':
    u = user_data()
    # 评论过十万的歌曲歌单
    # u.get_playlist_songs(376493212)
    # 评论过五万的歌曲歌单
    # u.get_playlist_songs(455717860)
    # u.get_song_comments(song_start=100, song_count=200)
    u.get_user_songs(user_start=6000, user_count=7000)
