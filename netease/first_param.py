# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------
import config


class first_param:
    """
    decrypt类中第一个请求参数的获取

    """

    def get_first_param(self, param_type, user_id="", search_keywords="", search_type=config.aes_search_type):
        """
        获取第一个参数

        :param param_type: 获取参数类型,详见config
        :param user_id: 用户id（可选）
        :param search_keywords: 搜索关键字（可选）
        :param search_type: 搜索类型（可选），详见config
        :return: status:是否成功获取
        :return:请求参数
        """
        if param_type == config.aes_param_comment:
            return True, self.get_first_param_comment()
        elif param_type == config.aes_param_ranklist:
            return True, self.get_first_param_ranklist(user_id)
        elif param_type == config.aes_param_search:
            return True, self.get_first_param_search(search_keywords=search_keywords, search_type=search_type)
        else:
            return False, ""

    def get_first_param_comment(self, total=config.aes_total, offset=config.aes_offset,
                                limit=config.aes_limit_page):
        """
        歌曲评论参数

        :param total: 目前暂时没发现影响，true or false
        :param offset: 偏移量，默认0
        :param limit:  返回的评论数每一页评论个数限制
        :return: status:是否成功获取
        :return: 请求参数
        """
        return True, """{{rid:"{}",offset:"{}",total:"{}",limit:"{}",csrf_token:"{}"}}""" \
            .format("", offset, total, limit, "")

    def get_first_param_ranklist(self, user_id=config.user_id, total=config.aes_total, offset=config.aes_offset,
                                 limit=config.aes_limit, type=config.aes_ranklist_type):
        """
        用户排行榜参数

        :param user_id: 用户id
        :param total: 目前暂时没发现影响，true or false
        :param offset: 偏移量，默认0
        :param limit: 限制数
        :param type: 类型
        :return: status:是否成功获取
        :return: 请求参数
        """
        return True, """{{uid:"{}",offset:"{}",total:"{}",limit:"{}",type:"{}",csrf_token:"{}"}}""" \
            .format(user_id, offset, total, limit, type, "")

    def get_first_param_search(self, search_keywords="", search_type=config.aes_search_type, offset=config.aes_offset,
                               limit=config.aes_limit):
        """
        搜索表单参数

        :param search_keywords: 搜索关键字
        :param search_type: 搜索类型,详见config
        :return: status:是否成功获取
        :return: 请求参数
        """
        return True, """{{s:"{}",type:"{}",limit:"{}",offset:"{}"}}""" \
            .format(search_keywords, search_type, limit, offset)


if __name__ == '__main__':
    r = first_param()
    print(r.get_first_param_comment())
    print(r.get_first_param_ranklist())
    print(r.get_first_param_search("test", 1002))
