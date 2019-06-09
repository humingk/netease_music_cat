# !/usr/bin/env python
# -*- coding: utf-8 -*-

import config
import requests
import json

"""
传入user_id,返回用户首页的“最后一周”和“所有时间”排行榜共200首歌单的song列表
待优化:
    分析core.js文件
    通过crypto中的AES解决param和encSecKey两个加密参数，参见decrypt模块
"""


class ranklist:

    def __init__(self):
        # 歌单列表
        self.ranklists_id = []

        base_url = config.base_url
        host = config.host
        user_agent = config.user_agent
        accept = config.accept

        cookie_ranklist = config.cookie_ranklist

        self.headers = {
            "Referer": base_url,
            "Host": host,
            "User-Agent": user_agent,
            "Accept": accept,
            "Cookie": cookie_ranklist
        }

    def get_ranklists_id(self, user_id):
        params_ranklist = config.params_ranklist
        encSecKey_ranklist = config.encSecKey_ranklist
        self.user_data = {
            "uid": user_id,
            "type": "0",
            "params": params_ranklist,
            "encSecKey": encSecKey_ranklist
        }
        # url = "https://music.163.com/#/user/songs/?id=" + user_id + "rank"
        url = 'http://music.163.com/weapi/v1/play/record?csrf_token='
        self.user_data['uid'] = user_id
        self.user_data['type'] = '0'
        response = requests.post(url, headers=self.headers, data=self.user_data)
        response = response.content
        json_text = json.loads(response.decode("utf-8"))

        json_all_data = json_text["allData"]
        json_week_data = json_text["weekData"]

        for i in range(len(json_all_data)):
            self.dict_save((json_all_data[i]["song"]["id"]), json_all_data[i]["song"]["name"])
        for i in range(len(json_week_data)):
            self.dict_save((json_week_data[i]["song"]["id"]), json_week_data[i]["song"]["name"])

        return self.ranklists_id

    def dict_save(self, song_id, song_name):
        self.ranklists_id.append({
            "song_id": song_id,
            "song_name": song_name
        })


if __name__ == "__main__":
    hl = ranklist()
    user_id = "55494140"
    print(hl.get_ranklists_id(user_id))
