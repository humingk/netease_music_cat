# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------
import json
import time
import config
from my_tools.logger_tool import loggler_tool
from my_tools.database_pool import database_pool
from netease.first_param import first_param
from netease.request_data import request_data
from my_tools.thread_pool import thread_pool

logger = loggler_tool()


class song_comments:
    """
    歌曲评论获取类

    """

    def get_song_comments_hot(self, song_id, song_comments_hot_max=config.song_comments_hot_max,
                              thread_count=config.song_comments_thread_count,
                              thread_inteval_time=config.song_comments_thread_thread_inteval_time,
                              song_comments_page_limit=config.song_comments_page_limit):
        """
        通过song_id获取热门评论

        :param song_id: 歌曲id
        :param song_comments_hot_max: 热门评论最大数(默认-1无限)
        :param thread_count: 线程数
        :param thread_inteval_time: 间隔时间
        :param song_comments_page_limit: 每页限制数
        """
        # 获取热门评论总数
        content = self.get_song_comments_total(song_id=song_id, comment_type=config.song_comments_type_hot)
        comments_total = 0
        if content[0]:
            comments_total = content[1]
        # 获取所有热门评论
        if song_comments_hot_max == -1:
            song_comments_hot_max = comments_total + 1
        # 多线程获取热门评论
        pool = database_pool()
        try:
            _thread_pool = thread_pool(thread_max=thread_count)
            max = comments_total if comments_total < song_comments_hot_max else song_comments_hot_max
            for page in range(0, max, song_comments_page_limit):
                _thread_pool.add(func=self.get_song_page_comments,
                                 args=(
                                     song_id, pool, config.song_comments_type_default, page, song_comments_page_limit),
                                 callback=None)
                time.sleep(thread_inteval_time)
            _thread_pool.close()
            logger.info(
                "get_song_comments_hot success", "song_id:{},comments_total:{},pages_total:{},page_comments_limit:{}"
                    .format(song_id, comments_total, max / song_comments_page_limit,
                            song_comments_page_limit))
            return True
        except Exception as e:
            logger.error(
                "get_song_comments_hot failed", "song_id:{},comments_total:{},error:{}"
                    .format(song_id, comments_total, e))

    def get_song_comments_default(self, song_id, thread_count=config.song_comments_thread_count,
                                  thread_inteval_time=config.song_comments_thread_thread_inteval_time,
                                  song_comments_new_max=config.song_comments_new_max,
                                  song_comments_old_max=config.song_comments_old_max,
                                  song_comments_page_limit=config.song_comments_page_limit):
        """
        通过song_id获取标准评论

        :param song_id: 歌曲id
        :param thread_count: 多线程个数
        :param thread_inteval_time: 间隔时间
        :param song_comments_new_max: 最新评论最大数,详见config
        :param song_comments_old_max: 最旧评论最大数,详见config
        :param song_comments_page_limit: 每一页获取标准评论数限制
        """
        # 获取标准评论总数
        content = self.get_song_comments_total(song_id=song_id, comment_type=config.song_comments_type_default)
        comments_total = 0
        if content[0]:
            comments_total = content[1]
        # 多线程获取最新评论+最老评论
        pool = database_pool()
        try:
            _thread_pool = thread_pool(thread_max=thread_count)
            # new_pages与old_pages不相交
            if song_comments_new_max <= comments_total - song_comments_old_max:
                new_pages = list(range(0, song_comments_new_max, song_comments_page_limit))
                old_pages = list(
                    range(comments_total - song_comments_old_max, comments_total, song_comments_page_limit))
            # 相交
            else:
                new_pages = list(range(0, comments_total, song_comments_page_limit))
                old_pages = []
            for page in set(new_pages + old_pages):
                _thread_pool.add(func=self.get_song_page_comments,
                                 args=(
                                     song_id, pool, config.song_comments_type_default, page, song_comments_page_limit),
                                 callback=None)
                time.sleep(thread_inteval_time)
            _thread_pool.close()
            logger.info(
                "get_song_comments_normal success", "song_id:{},comments_total:{},pages_total:{},page_comments_limit:{}"
                    .format(song_id, comments_total, len(set(new_pages + old_pages)), song_comments_page_limit))
            return True
        except Exception as e:
            logger.error(
                "get_song_comments_normal failed", "song_id:{},comments_total:{},error:{}"
                    .format(song_id, comments_total, e))
            return False

    def get_song_comments_total(self, song_id, comment_type=config.song_comments_type_hot):
        """
        获取评论总数

        :param song_id: 歌曲id
        :param comment_type: 评论类型
        :return: 评论总数
        """
        content = self.get_song_page_comments(song_id=song_id, comment_type=comment_type, is_get_comment_total=True)
        try:
            if content[0]:
                pool = database_pool()
                pool.insert_song(song_id=song_id)
                pool.commit()
                if comment_type == config.song_comments_type_hot:
                    pool.update_song_hot_comment_count(song_id=song_id, song_hot_comment_count=content[1])
                elif comment_type == config.song_comments_type_default:
                    pool.update_song_default_comment_count(song_id=song_id, song_default_comment_count=content[1])
                pool.commit()
                return True, content[1]
        except Exception as e:
            logger.error("get_song_comments_total_count failed",
                         "song_id:{},comment_type:{},error:{}".format(song_id, comment_type, e))
            return False, []

    def get_song_page_comments(self, song_id, pool=None, comment_type=config.song_comments_type_hot, offset=0, limit=0,
                               is_get_comment_total=False):
        """
        通过song_id获取某页评论

        :param song_id: 歌曲id
        :param pool: 数据库连接池
        :param comment_type: 评论类型,详见config
        :param offset: 位移量
        :param limit: 每页评论限制量
        :param is_get_comment_total: 是否为获取评论总数，默认否
        :return: 评论数据
        """
        # 获取请求参数
        _first_param = first_param().get_first_param_eapi_comment(offset=offset, limit=limit)
        if comment_type == config.song_comments_type_hot:
            url = config.get_comments_hot_url(song_id)
            eapi_url = config.get_comment_hot_url_for_eapi_param(song_id)
        elif comment_type == config.song_comments_type_default:
            url = config.get_comments_default_url(song_id)
            eapi_url = config.get_comment_default_url_for_eapi_param(song_id)
        else:
            return False, None
        # 请求数据
        content = request_data().get_request_data(first_param=_first_param[1], url=url, api_type=config.api_eapi,
                                                  eapi_url=eapi_url)
        # 解析数据
        try:
            if content[0]:
                if is_get_comment_total:
                    return True, json.loads(content[1])["total"]
                elif comment_type == config.song_comments_type_default:
                    json_data = json.loads(content[1])["comments"]
                elif comment_type == config.song_comments_type_hot:
                    json_data = json.loads(content[1])["hotComments"]
                else:
                    return False, None
            else:
                return False, None
        except Exception as e:
            logger.error("get_song_comments_page failed", "song_id:{},comment_type:{},offset:{},limit:{},error:{}"
                         .format(song_id, comment_type, offset, limit, e))
            return False, []
        # 存储数据
        comments_list = []
        for comment_json in json_data:
            comments_list.append(
                self.__add(song_id=song_id, comment_json=comment_json, pool=pool, comments_list=comments_list,
                           comment_type=config.song_comments_type_hot))
        pool.commit()
        return True, comments_list

    def __add(self, song_id, pool, comment_json, comments_list, comment_type=config.song_comments_type):
        """
        添加信息

        :param song_id: 歌曲id
        :param pool: 数据库线程池
        :param comment_json: 评论内容
        :param comments_list: 返回数据
        :param comment_type: 评论类型
        :return: 评论+用户信息
        """
        comment = {
            "comment_id": comment_json["commentId"],
            "comment_date": comment_json["time"],
            "comment_content": comment_json["content"],
            "comment_type": comment_type,
            "comment_like_count": comment_json["likedCount"]
        }
        user = {
            "user_id": comment_json["user"]["userId"],
            "user_name": comment_json["user"]["nickname"]
        }
        comments_list.append({"comment": comment, "user": user})
        pool.insert_user(user_id=user["user_id"], user_name=user["user_name"])
        pool.insert_comment(comment_id=comment["comment_id"], comment_type=comment["comment_type"],
                            comment_date=comment["comment_date"], comment_content=comment["comment_content"],
                            comment_like_count=comment["comment_like_count"])
        pool.insert_song_comment(song_id=song_id, comment_id=comment["comment_id"])
        pool.insert_user_comment(user_id=user["user_id"], comment_id=comment["comment_id"])


if __name__ == '__main__':
    print(song_comments().get_song_comments_total(song_id=31445772, comment_type=config.song_comments_type_hot))
    print(song_comments().get_song_comments_total(song_id=31445772, comment_type=config.song_comments_type_default))
    # song_comments().get_song_comments_hot(song_id=31445772, song_comments_hot_max=500, thread_count=20,
    #                                       thread_inteval_time=0.2, song_comments_page_limit=100)
    song_comments().get_song_comments_default(song_id=31445772, thread_count=20, thread_inteval_time=0.2,
                                              song_comments_new_max=500, song_comments_old_max=500,
                                              song_comments_page_limit=100)
