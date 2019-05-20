# !/usr/bin/env python
# -*- coding: utf-8 -*-

import config
import requests
import json
import decrypt

from neteast_mine.config import encSecKey_play_lists

"""
    歌单获取模块
        使用方法：
            get_lists_id(user_id)
        
        传入user_id
        返回用户首页所有歌单的id

"""


class playlists:

    def __init__(self):
        # 歌单的id列表
        self.lists_id = []

    def get_lists_id(self, user_id):
        json_text = json.loads(decrypt.get_json(url=config.url_playlists, param_type="songs", total=True, offset=0, proxies=""))
        json_playlists_data = json_text["playlist"]

        i = 0
        while i < config.playlists_max and i < len(json_playlists_data):
            if (config.only_playlists_created):
                # 只爬取用户自己创建的歌单
                if str(json_playlists_data[i]["creator"]['userId']) == str(user_id):
                    self.lists_id.append(json_playlists_data[i]["id"])
            else:
                self.lists_id.append(json_playlists_data[i]["id"])
            i += 1

        return self.lists_id


if __name__ == "__main__":
    user_id = "55494140"
    print(playlists().get_lists_id(user_id))
