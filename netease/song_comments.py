# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------
import json
import time
import config
from my_tools.logger_tool import loggler_tool
from my_tools.database_tool import database_tool
from netease.first_param import first_param
from netease.request_data import request_data
from my_tools.thread_pool import thread_pool
from concurrent.futures import ThreadPoolExecutor, as_completed

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

        # 多线程获取热门评论
        comments_page_success_count = 0
        try:
            # 若max为-1,获取所有热门评论
            if song_comments_hot_max == -1:
                song_comments_hot_max = comments_total + 1
            comments_max = comments_total if comments_total < song_comments_hot_max else song_comments_hot_max
            with ThreadPoolExecutor(thread_count) as executer:
                future_to_result = {
                    executer.submit(self.get_song_page_comments, song_id, config.song_comments_type_hot, page,
                                    song_comments_page_limit): page for
                    page in range(0, comments_max, song_comments_page_limit)
                }
                for future in as_completed(future_to_result):
                    if future_to_result[future] is not None:
                        comments_page_success_count += 1
            logger.info(
                "get_song_comments_hot success",
                "song_id:{},comments_total:{},comments_page_success_total:{},page_comments_limit:{}"
                    .format(song_id, comments_total, comments_page_success_count, song_comments_page_limit))
            return True
        except Exception as e:
            logger.error(
                "get_song_comments_hot failed",
                "song_id:{},comments_total:{},comments_page_success_total:{},error_type:{},error:{}"
                    .format(song_id, comments_total, comments_page_success_count, type(e), e))
        return False

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
        comments_page_success_total = 0
        try:
            # new_pages与old_pages不相交
            if song_comments_new_max <= comments_total - song_comments_old_max:
                new_pages = list(range(0, song_comments_new_max, song_comments_page_limit))
                old_pages = list(
                    range(comments_total - song_comments_old_max, comments_total, song_comments_page_limit))
            # new_pages与old_pages相交
            else:
                new_pages = list(range(0, comments_total, song_comments_page_limit))
                old_pages = []
            with ThreadPoolExecutor(thread_count) as executer:
                future_to_result = {
                    executer.submit(self.get_song_page_comments, song_id, config.song_comments_type_default, page,
                                    song_comments_page_limit): page for page in set(new_pages + old_pages)
                }
                for future in as_completed(future_to_result):
                    if future_to_result[future] is not None:
                        comments_page_success_total += 1
            logger.info(
                "get_song_comments_default success",
                "song_id:{},comments_total:{},pages_total:{},comments_page_success_total:{},page_comments_limit:{}"
                    .format(song_id, comments_total, len(set(new_pages + old_pages)), comments_page_success_total,
                            song_comments_page_limit))
            return True
        except Exception as e:
            logger.error(
                "get_song_comments_default failed",
                "song_id:{},comments_total:{},comment_page_success_total,error_type:{},error:{}"
                    .format(song_id, comments_total, comments_page_success_total, type(e), e))
        return False

    def get_song_comments_total(self, song_id, comment_type=config.song_comments_type_hot):
        """
        获取评论总数

        :param song_id: 歌曲id
        :param comment_type: 评论类型
        :return: 评论总数
        """
        # 获取数据
        content = self.get_song_page_comments(song_id=song_id, comment_type=comment_type, is_get_comment_total=True)
        # 解析+存储数据
        try:
            if content[0]:
                _database_tool = database_tool()
                _database_tool.insert_many_song([[song_id, '']])
                _database_tool.commit()
                if comment_type == config.song_comments_type_hot:
                    _database_tool.update_song_hot_comment_count(song_id=song_id, song_hot_comment_count=content[1])
                elif comment_type == config.song_comments_type_default:
                    _database_tool.update_song_default_comment_count(song_id=song_id,
                                                                     song_default_comment_count=content[1])
                _database_tool.commit()
                _database_tool.close()
                logger.info("get_song_comments_total success", "song_id:{},comment_type:{},comment_total:{}"
                            .format(song_id, comment_type, content[1]))
                return True, content[1]
        except Exception as e:
            logger.error("get_song_comments_total_count failed",
                         "song_id:{},comment_type:{},error_type:{},error:{}".format(song_id, comment_type, type(e), e))
        return False, None

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
            logger.error("get_song_page_comments failed",
                         "song_id:{},comment_type:{},offset:{},limit:{},error_type:{},error:{}"
                         .format(song_id, comment_type, offset, limit, type(e), e))
            return False, []
        # 解析数据
        user_list = []
        comment_list = []
        user_comment_list = []
        song_comment_list = []
        try:
            for comment_json in json_data:
                # user_id user_name
                user_list.append([
                    comment_json["user"]["userId"],
                    comment_json["user"]["nickname"]
                ])
                # comment_id comment_type comment_date comment_content comment_like_count
                comment_list.append([
                    comment_json["commentId"],
                    comment_type,
                    comment_json["time"],
                    comment_json["content"],
                    comment_json["likedCount"]
                ])
                # user_id comment_id
                user_comment_list.append([
                    comment_json["user"]["userId"],
                    comment_json["commentId"]
                ])
                # song_id comment_id
                song_comment_list.append([
                    song_id,
                    comment_json["commentId"]
                ])
            logger.info("get_song_page_comments parse success",
                        "song_id:{},comment_total:{},comment_type:{},offset:{},limit:{}"
                        .format(song_id, len(comment_list), comment_type, offset, limit))
        except Exception as e:
            logger.error("get_song_page_comments parse failed",
                         "song_id:{},comment_type:{},offset:{},limit:{},error_type:{},error:{}"
                         .format(song_id, comment_type, offset, limit, type(e), e))
        # 存储数据
        try:
            _database_tool = database_tool()
            _database_tool.insert_many_user(user_list)
            _database_tool.insert_many_comment(comment_list)
            _database_tool.commit()
            _database_tool.insert_many_song_comment(song_comment_list)
            _database_tool.insert_many_user_comment(user_comment_list)
            _database_tool.commit()
            _database_tool.close()
        except Exception as e:
            logger.error("get_song_page_comments save failed",
                         "song_id:{},comment_type:{},offset:{},limit:{},error_type:{},error:{}"
                         .format(song_id, comment_type, offset, limit, type(e), e))
        return True, (user_list, comment_list, user_comment_list)


if __name__ == '__main__':
    # print(song_comments().get_song_comments_total(song_id=31445772, comment_type=config.song_comments_type_hot))
    # print(song_comments().get_song_comments_total(song_id=31445772, comment_type=config.song_comments_type_default))
    song_comments().get_song_comments_hot(song_id=31445772, song_comments_hot_max=1000, thread_count=20,
                                          thread_inteval_time=0.2, song_comments_page_limit=100)
    # song_comments().get_song_comments_default(song_id=31445772, thread_count=20, thread_inteval_time=0.2,
    #                                           song_comments_new_max=500, song_comments_old_max=500,
    #                                           song_comments_page_limit=100)
