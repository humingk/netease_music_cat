# !/usr/bin/env python
# -*- coding: utf-8 -*-

import config
import bs4
import requests

"""
传入歌单的id，返回歌单所有歌的song信息

"""


class playlist:

    def __init__(self):
        # 歌曲列表
        self.playlist_songs = []

        base_url = config.base_url
        host = config.host
        user_agent = config.user_agent
        accept = config.accept

        self.headers = {
            "Referer": base_url,
            "Host": host,
            "User-Agent": user_agent,
            "Accept": accept
        }

    def get_playlist_songs_id(self, playlist_id):
        playlist_url = "https://music.163.com/playlist?id=" + str(playlist_id)

        resquest_obj = requests.session()
        response_obj = resquest_obj.get(playlist_url, headers=self.headers)
        bs_obj = bs4.BeautifulSoup(response_obj.content)
        songs_obj = bs_obj.find("ul", {"class": "f-hide"})

        for song in songs_obj.find_all("a"):
            # song="<a href="/song?id=1518938">As Long As You Love Me</a>"
            song_name = song.get_text()
            song_id = song["href"][9:]
            self.dict_save(song_id, song_name)

        return self.playlist_songs

    def dict_save(self, song_id, song_name):
        self.playlist_songs.append({
            "song_id": song_id,
            "song_name": song_name
        })


if __name__ == "__main__":
    pl = playlist()
    x = pl.get_playlist_songs_id("54125412")
    print(len(x))
    print(x)
