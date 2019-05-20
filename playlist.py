# !/usr/bin/env python
# -*- coding: utf-8 -*-

import config
import bs4
import requests

"""
    歌单歌曲获取模块
        使用方法：
            get_playlist_songs_id(playlist_id,isLike)
            
        传入歌单的id,是否是用户喜欢的音乐歌单
        返回歌单歌曲列表信息

"""


class playlist:

    def __init__(self):
        # 歌曲列表
        self.playlist_songs = []

    def get_playlist_songs_id(self, playlist_id, isLike):
        response = requests.session().get(config.get_playlist_url(playlist_id), headers=config.user_headers).content
        bs = bs4.BeautifulSoup(response,"lxml")
        songs = bs.find("ul", {"class": "f-hide"})

        i = 0
        for song in songs.find_all("a"):
            if (isLike == False and i >= config.playlist_songs_max):
                break
            # song="<a href="/song?id=1518938">As Long As You Love Me</a>"
            song_name = song.get_text()
            song_id = song["href"][9:]
            self.playlist_songs.append({
                "song_id": song_id,
                "song_name": song_name
            })
            i += 1

        return self.playlist_songs


if __name__ == "__main__":
    print(playlist().get_playlist_songs_id("13928655", False))
