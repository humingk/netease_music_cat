# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------
import json

import config


class first_param:
    """
    decrypt类中第一个请求参数的获取

    """

    def get_first_param_weapi_comment(self, offset=config.aes_offset, limit=config.song_comments_page_limit):
        """
        歌曲评论参数
        weapi

        :param offset: 偏移量，默认0
        :param limit:  返回的评论数每一页评论个数限制
        :return: status:是否成功获取
        :return: 请求参数
        """
        return True, """{{rid:"{}",offset:"{}",limit:"{}"}}""".format('', offset, limit)

    def get_first_param_eapi_comment(self, offset=config.aes_offset, limit=config.song_comments_page_limit):
        """
        歌曲热门评论参数
        eapi

        :param offset: 偏移量，默认0
        :param limit:  返回的评论数每一页评论个数限制
        :return: status:是否成功获取
        :return: 请求参数
        """
        params = config.eapi_params
        params['rid'] = ''
        params['offset'] = offset
        params['limit'] = limit
        return True, json.dumps(params, separators=(',', ':'))

    def get_first_param_ranklist(self, user_id=config.user_id, rank_type=config.rank_type):
        """
        用户排行榜参数

        :param user_id: 用户id
        :param rank_type: 排行榜类型，详见config
        :return: status:是否成功获取
        :return: 请求参数
        """
        return True, """{{uid:"{}",type:"{}"}}""".format(user_id, rank_type)

    def get_first_param_user_playlists(self, user_id=config.user_id, limit=config.aes_limit, offset=config.aes_offset):
        """
        用户所有歌单参数

        :param user_id: 用户id
        :param limit: 用户歌单最大数(此处无用，由user_playlists控制)
        :param offset: 位移
        :return: status:是否成功获取
        :return: 请求参数
        """
        return True, """{{uid:"{}",limit:"{}",offset:"{}"}}""".format(user_id, limit, offset)

    def get_first_param_playlist(self, playlist_id=config.playlist_id, n=100000, s=0):
        """
        歌单参数

        :param playlist_id: 歌单id
        :param n: ?
        :param s: 歌单最近的收藏者
        :return: status:是否成功获取
        :return: 请求参数
        """
        return True, """{{id:"{}",n:"{}",s:"{}"}}""".format(playlist_id, n, s)

    def get_first_param_search(self, search_keywords="", search_type=config.search_type, offset=config.aes_offset,
                               limit=30):
        """
        搜索表单参数

        :param search_keywords: 搜索关键字
        :param search_type: 搜索类型,详见config
        :param offset: 偏移量
        :param limit: 返回个数
        :return: status:是否成功获取
        :return: 请求参数
        """
        return True, """{{s:"{}",type:"{}",limit:"{}",offset:"{}"}}""" \
            .format(search_keywords, search_type, limit, offset)


if __name__ == '__main__':
    r = first_param()
    print(r.get_first_param_ranklist())
    print(r.get_first_param_user_playlists())
    print(r.get_first_param_search("test", 1002))
    print(r.get_first_param_weapi_comment(offset=0, limit=15))
    print(r.get_first_param_eapi_comment(offset=0, limit=15))
