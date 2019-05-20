# !/usr/bin/env python
# -*- coding: utf-8 -*-

import config
import requests
import json
import decrypt

"""
排行榜模块
    使用方法：
        get_ranklists_id(user_id)
        
        传入user_id
        返回用户首页的“最后一周”和“所有时间”排行榜歌单的歌曲列表

"""


class ranklist:

    def __init__(self):
        # 歌单列表
        self.ranklists_id = []

    # 获取歌单歌曲列表
    def get_ranklists_id(self, user_id):
        json_text=json.loads(decrypt.get_json(url=config.url_rank, param_type="songs", total=True, offset=0, proxies=""))

        json_all_data = json_text["allData"]
        json_week_data = json_text["weekData"]

        i = 0
        while i < config.rank_all_max and i < len(json_all_data):
            self.ranklists_id.append({
                "song_id": json_all_data[i]["song"]["id"],
                "song_name": json_all_data[i]["song"]["name"]
            })
            i += 1
        j = 0
        while j < config.rank_week_max and j < len(json_week_data):
            self.ranklists_id.append({
                "song_id": json_week_data[j]["song"]["id"],
                "song_name": json_week_data[j]["song"]["name"]
            })
            j += 1

        return self.ranklists_id


if __name__ == "__main__":
    user_id = "55494140"
    print(ranklist().get_ranklists_id(user_id))
