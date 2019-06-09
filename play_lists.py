# !/usr/bin/env python
# -*- coding: utf-8 -*-

import config
import requests
import json

"""
传入user_id,返回用户首页所有歌单的id
待优化:
    分析core.js文件
    通过crypto中的AES解决param和encSecKey两个加密参数，参见decrypt模块

"""


class play_lists:

    def __init__(self):
        # 歌单的id列表
        self.lists_id = []

        base_url = config.base_url
        host = config.host
        user_agent = config.user_agent
        accept = config.accept
        cookie_play_lists = config.cookie_play_lists

        self.headers = {
            "Referer": base_url,
            "Host": host,
            "User-Agent": user_agent,
            "Accept": accept,
            "Cookie": cookie_play_lists
        }

    def get_lists_id(self, user_id):
        params_play_lists = config.params_play_lists
        encSecKey_play_lists = config.encSecKey_play_lists
        self.user_data = {
            "uid": user_id,
            "type": "0",
            "params": params_play_lists,
            "encSecKey": encSecKey_play_lists
        }
        url = "https://music.163.com/weapi/user/playlist?csrf_token="
        self.user_data['uid'] = user_id
        self.user_data['type'] = '0'
        response = requests.post(url, headers=self.headers, data=self.user_data)
        response = response.content
        json_text = json.loads(response.decode("utf-8"))

        # print(json_text)
        json_playlists_data = json_text["playlist"]

        #爬取用户首页所有的歌单
        # for i in range(len(json_playlists_data)):
        # print(str(json_playlists_data[i]["id"]))
        # self.lists_id.append(json_playlists_data[i]["id"])

        # 只爬取用户自己创建的歌单，包括喜欢的歌
        for i in range(len(json_playlists_data)):
            if str(json_playlists_data[i]["creator"]['userId']) == str(user_id):
                self.lists_id.append(json_playlists_data[i]["id"])

        return self.lists_id


if __name__ == "__main__":
    hl = play_lists()
    user_id = "55494140"
    print(hl.get_lists_id(user_id))
