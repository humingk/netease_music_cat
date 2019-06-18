# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------
import json

import pymysql

import config
from netease.first_param import first_param
from netease.request_data import request_data
from database_pool import database_pool
from logger_tool import loggler_tool

logger = loggler_tool()


class comment_pages:
    """
    评论页获取类

    """

    def __init__(self):
        self.page_comments_list = []

    def get_song_page_comments(self, song_id, comment_type=config.song_comments_type_hot, offset=0, limit=0,
                               is_get_comment_total=False):
        """
        通过song_id获取某页评论

        :param song_id: 歌曲id
        :param comment_type: 评论类型,详见config
        :param offset: 位移量
        :param limit: 每页评论限制量
        :param is_get_comment_total: 是否为获取评论总数，默认否
        :return: 评论数据
        """
        # 请求参数
        _first_param = first_param().get_first_param_comment(offset=offset, limit=limit)
        # 请求数据
        content = request_data().get_request_data(first_param=_first_param[1], url=config.get_comments_url(song_id))
        try:
            if content[0]:
                if is_get_comment_total:
                    return True, json.loads(content[1])["total"]
                elif comment_type == config.song_comments_type_default:
                    json_data = json.loads(content[1])["comments"]
                elif comment_type == config.song_comments_type_hot:
                    json_data = json.loads(content[1])["hotComments"]
                else:
                    return False, []
            else:
                return False, []
        except Exception as e:
            logger.error("get_song_comments_page failed", "song_id:{},comment_type:{},offset:{},limit:{},error:{}"
                         .format(song_id, comment_type, offset, limit, e))
            return False, []
        pool = database_pool()
        for comment_json in json_data:
            self.__add(comment_json=comment_json, pool=pool, comment_type=config.song_comments_type_hot)
        pool.commit()
        return True, self.page_comments_list

    def __add(self, comment_json, pool, comment_type=config.song_comments_type):
        """
        添加信息

        :param comment_json: 评论内容
        :param pool: 数据库线程池
        :param comment_type: 评论类型
        """
        comment = {
            "comment_id": comment_json["commentId"],
            "comment_date": comment_json["time"],
            "comment_content": comment_json["content"],
            "comment_type": comment_type
        }
        user = {
            "user_id": comment_json["user"]["userId"],
            "user_name": comment_json["user"]["nickname"]
        }
        self.page_comments_list.append(comment)
        pool.execute(
            "insert into comment(comment_id, comment_date,comment_content,comment_type) values('{}',{},'{}',{})"
                .format(comment["comment_id"], comment["comment_date"],
                        pymysql.escape_string(comment["comment_content"]), comment["comment_type"]))
        pool.execute(
            "insert into user(user_id, user_name) values('{}','{}')"
                .format(user["user_id"], pymysql.escape_string(user["user_name"]))
        )
        pool.execute(
            "insert into user_comment(user_id, comment_id) values ('{}','{}')"
                .format(user["user_id"], comment["comment_id"])
        )


if __name__ == '__main__':
    comment_pages().get_song_page_comments(config.song_id, comment_type=config.song_comments_type_hot)
