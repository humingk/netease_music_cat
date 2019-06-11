# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------
from netease.decrypt import decrypt
import logger
log=logger.loggler()

class user:
    """
    获取用户基本信息类

    """
    def __init__(self):
        self.user_id=0

    def get_user_id(self,user_name):
        """
        通过用户名获取用户id

        :param user_name: 用户名

        """
        content=decrypt().get_json()
        if content[0]:
            json_text=content[1]
        else:
            return False,None
        print(json_text)

if __name__ == '__main__':
    user().get_user_id("小明也来过")
