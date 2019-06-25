# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------
import json
import config
from netease.search import search
from my_tools.logger_tool import loggler_tool

logger = loggler_tool()


class user_message:
    """
    获取用户信息

    """

    def get_user_by_name(self, user_name=config.user_name):
        """
        通过用户昵称获取用户id

        :param user_name: 用户昵称
        :return: status:获取状态
        :return: 用户信息
        """
        search_result = search().get_search(search_keyword=user_name, search_type=config.search_type_user)
        user_message = []
        if search_result[0]:
            user = json.loads(search_result[1])["result"]["userprofiles"][0]
            print(user)
        else:
            logger.debug("get_user_by_name failed", "user_name:{}".format(user_name))
            return False, []
        user_message.append({
            "user_id": user["userId"],
            "user_name": user_name
        })
        logger.debug("get_user_by_name success", "user_name:{},user_id:{}".format(user_name, user["userId"]))
        return True, user_message

    def get_user_by_id(self, user_id=config.user_id):
        pass


if __name__ == '__main__':
    print(user_message().get_user_by_name())
    print(user_message().get_user_by_id())
