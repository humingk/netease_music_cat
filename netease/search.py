# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------
import config
from netease.first_param import first_param
from netease.request_data import request_data
from logger_tool import loggler_tool

logger = loggler_tool()


class search:
    """
    搜索类

    """

    def get_search(self, search_keyword="", search_type=config.search_type):
        """
        关键字搜索

        :param search_keyword: 搜索关键字
        :param search_type: 搜索类型
        :return: status:搜索状态
        :return: 搜索结果
        """
        _first_param = first_param().get_first_param_search(search_keywords=search_keyword, search_type=search_type)
        content = request_data().get_request_data(first_param=_first_param[1], url=config.url_search)
        if content[0]:
            json_data = content[1]
        else:
            return False, None
        logger.debug("get_search success", "search_keyword:{},search_type:{}".format(search_keyword, search_type))
        return True, content[1]


if __name__ == '__main__':
    print(search().get_search("小明也来过", config.search_type_user))
