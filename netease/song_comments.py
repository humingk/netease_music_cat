# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------
import json

import config
from logger import loggler
from netease.first_param import first_param
from netease.request_data import request_data

log = loggler()


class song_comments:
    """
    歌曲评论获取类

    """

    def __init__(self):
        self.comments_list = []

    def get_song_comments_hot(self, song_id):
        """
        通过song_id获取热门评论

        :param song_id: 歌曲id
        """
        content = self.get_song_comments_page(song_id=song_id, offset=config.aes_offset, limit=0)
        try:
            if not content[0]:
                return False, []
        except Exception as e:
            log.error("get_song_comments_hot failed", "song_id:{},error:{}".format(song_id, e))
            return False,[]


    def get_song_comments(self, song_id):
        """
        通过song_id获取评论

        :param song_id: 歌曲id
        """

    def get_song_comments_page(self, song_id, offset, limit):
        """
        通过song_id获取某页评论

        :param song_id: 歌曲id
        :param offset: 位移量
        :param limit: 每页评论限制量
        :return: 评论数据
        """
        # 请求参数
        _first_param = first_param().get_first_param_comment(offset=offset, limit=limit)
        # 请求数据
        content = request_data().get_request_data(first_param=_first_param[1], url=config.get_comments_url(song_id))
        try:
            if content[0]:
                json_data = json.loads(content[1])
            else:
                return False, []
        except Exception as e:
            log.error("get_song_comments_page failed", "song_id:{},error:{}".format(song_id, e))
            return False, []
        return True, json_data


if __name__ == '__main__':
    song_comments().get_song_comments(config.song_id)
