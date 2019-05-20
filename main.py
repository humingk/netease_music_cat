# !/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import time
from threading import Timer
import multiprocessing
import config
import decrypt
import pymysql
import playlist
import ranklist
import play_lists
import warnings
import sqlite3

import ProxiesDataBase
import Util

"""
    

爬虫某首歌的所有评论，添加到user_data和comment_data字典中
分离解码功能到decrypt模块
将comment_v2改为类
将user_data和comment_data字典添加到mysql中
修复v1_v4中offset偏移量在一个第一次执行一个page_limit后产生的错误
eg:第97条之后的comment每行固定偏移一个page_limit

"""
warnings.filterwarnings("ignore")


class comment:

    def __init__(self):

        # 评论内容
        self.comment_data = []
        # 评论用户
        self.user_data = []
        # 评论总数
        self.comment_sum = 0

        self.playlist = playlist.playlist()
        self.ranklist = ranklist.ranklist()
        self.play_lists = play_lists.play_lists()

    # 将13位的时间转化为10位
    def time_stamp(self, time_13):
        time_stamp = float(time_13 / 1000)
        time_array = time.localtime(time_stamp)
        time_10 = time.strftime("%Y-%m-%d %H:%M:%S", time_array)
        return time_10

    # 获取song_id这首歌下所有的评论
    def get_comments(self, song):

        song_id = song["song_id"]
        song_name = song["song_name"]

        print("ID:    " + str(song_id))
        print("歌名:  " + str(song_name))

        # 获取第一页中header中的Form Data数据项
        first_param = config.first_param
        params_obj_1 = decrypt.get_params(first_param)
        encSecKey_obj_1 = decrypt.get_encSecKey()

        url = "http://music.163.com/weapi/v1/resource/comments/R_SO_4_" + str(song_id) + "?csrf_token="

        # 代理IP
        print("正在验证代理IP中...")
        Util.Refresh()
        # 查询IP数据库多少条数据
        conn = sqlite3.connect(config.DBName)
        cu = conn.cursor()
        ip_num = cu.execute("""SELECT * FROM {};""".format(config.TabelName)).fetchall().__len__()
        print("共 " + str(ip_num) + " 个代理IP可用...")
        cu.close()
        conn.close()

        proxies = Util.Get()
        print("匿名IP代理成功...")
        print("ip: " + str(proxies["http"]))

        # 获取第一页中response中的json数据项
        json_text_1 = decrypt.get_json(url, params_obj_1, encSecKey_obj_1, proxies)
        json_obj_1 = json.loads(json_text_1)

        # 获取第一页的置顶评论
        if json_obj_1["topComments"]:
            for item in json_obj_1["topComments"]:
                self.dict_save(item, song_name)

        # 获取第一页的热门评论
        if json_obj_1["hotComments"]:
            for item in json_obj_1["hotComments"]:
                self.dict_save(item, song_name)

        # 评论总数
        self.comment_sum = int(json_obj_1["total"])

        # 每首歌最多20000条评论
        # 循环每一页的最新评论
        page_limit = config.page_limit
        if self.comment_sum<10000:
            for offset in range(int(page_limit), int(self.comment_sum), int(page_limit)):
                    # 若给定代理IP无法获取数据，循环执行
                    flag = True
                    while flag:
                        proxies = Util.Get()
                        flag = self.get_page_comment(proxies, offset, page_limit, url, song_name)
        else:
            # 正序10000条评论
            for offset in range(int(page_limit), 10000, int(page_limit)):
                # 若给定代理IP无法获取数据，循环执行
                flag = True
                while flag:
                    proxies = Util.Get()
                    flag = self.get_page_comment(proxies, offset, page_limit, url, song_name)
            # 倒序10000条评论
            for offset in range(int(self.comment_sum), int(self.comment_sum)-10000, -int(page_limit)):
                # 若给定代理IP无法获取数据，循环执行
                flag = True
                while flag:
                    proxies = Util.Get()
                    flag = self.get_page_comment(proxies, offset, page_limit, url, song_name)

        self.mysql_save()

    # 循环每一页的最新评论
    def get_page_comment(self, proxies, offset, page_limit, url, song_name):
        try:
            param_n = "{rid:\"\", offset:" + str(
                offset) + ", total:\"false\", limit:" + page_limit + ", csrf_token:\"\"}"
            # 获取第page页中header中的Form Data数据项
            params_obj_n = decrypt.get_params(param_n)
            encSecKey_obj_n = decrypt.get_encSecKey()

            # 获取第page页中response中的json数据项
            json_text_n = decrypt.get_json(url, params_obj_n, encSecKey_obj_n, proxies)
            json_obj_n = json.loads(json_text_n)
            if json_obj_n["comments"]:
                for item in json_obj_n["comments"]:
                    self.dict_save(item, song_name)
            return False
        except Exception as e:
            return True

    # 将这首歌下的评论存入字典
    def dict_save(self, item, song_name):
        print(str(len(self.user_data)) + " " + str(song_name) + "-->")
        self.user_data.append({
            "user_name": str(item["user"]["nickname"]),
            "user_id": str(item["user"]["userId"]),
            "comment_id": str(item["commentId"])
        })

        self.comment_data.append({
            "comment_id": str(item["commentId"]),
            "comment_song_name": song_name,
            "comment_content": str(item["content"]),
            "comment_time": str(self.time_stamp(item["time"]))
        })

    # 将字典存入mysql
    def mysql_save(self):

        # 连接数据库
        database_user_name = config.database_user_name
        database_user_pwd = config.database_user_pwd
        database_name = config.database_name
        database_charset = config.database_charset
        try:
            db = pymysql.connect("localhost", database_user_name, database_user_pwd, database_name,
                                 charset=database_charset)
        except pymysql.err as e:
            print("数据库连接失败！...")
            print(e)
        # 游标对象
        cursor = db.cursor()

        # comment_data数据
        table_comment_name = config.table_comment_name
        table_comment_cols = config.table_comment_cols

        for i in range(len(self.comment_data)):

            # 存放comment_data[i]中的value
            comment_values = []
            if self.comment_data is not None:
                for k, v in self.comment_data[i].items():
                    comment_values.append(v)

                comment_insert_sql = "INSERT IGNORE INTO %s (%s) VALUES (%s)" % (
                    str(table_comment_name), str(table_comment_cols), str(comment_values).strip("[]"))

                # 移除已经添加到数据库的comment_data字典元素
                delete_dict_comment = {}
                if self.comment_data is not None:
                    delete_dict_comment = self.comment_data[i]
                    # error :待修改
                    # del self.comment_data[i]

                try:
                    cursor.execute(comment_insert_sql)
                    db.commit()
                    if len(comment_insert_sql) % 1000 == 0:
                        print(str(len(comment_insert_sql)) + "-->")
                except pymysql.err as e:
                    print("插入数据表失败！...")
                    print(e)
                    db.rollback()

        # user_data数据
        table_user_name = config.table_user_name
        table_user_cols = config.table_user_cols

        for i in range(len(self.user_data)):

            # 存放user_data[i]中的value
            user_values = []
            if self.user_data is not None:
                for k, v in self.user_data[i].items():
                    user_values.append(v)

                user_insert_sql = "INSERT IGNORE INTO %s (%s) VALUES (%s)" % (
                    str(table_user_name), str(table_user_cols), str(user_values).strip("[]"))

                # 移除已经添加到数据库的user_data字典元素
                delete_dict_user = {}
                if self.user_data is not None:
                    delete_dict_user = self.user_data[i]
                    # del self.user_data[i]

                try:
                    cursor.execute(user_insert_sql)
                    db.commit()
                except pymysql.err as e:
                    print("插入数据表失败！...")
                    print(e)
                    db.rollback()

        # 关闭数据库
        db.close()

    # 控制台测试数据
    def output_data(self):
        for comment in self.comment_data:
            print("评论ID: " + comment["comment_id"])
            print("评论:   " + comment["comment_content"])
            print("时间:   " + comment["comment_time"])
            print("------------------")
        print("评论总数: " + str(self.comment_sum))

    # 定时刷新IP库
    def flash(self):
        Util.Refresh()
        t = Timer(300, self.flash)
        t.start()

if __name__ == "__main__":
    com = comment()
    user_id = config.user_id

    # 用户首页听歌排行榜所有歌
    print("正在爬取【所有时间】排行榜...")
    print("正在爬取【最近一周】排行榜...")
    rank_songs = com.ranklist.get_ranklists_id(user_id)

    # 用户首页所有歌单
    print("正在爬取用户的歌单...")
    playlists_id = com.play_lists.get_lists_id(user_id)

    # 用户首页所有歌单的歌
    playlists_songs = []
    for i in range(len(playlists_id)):
        playlist_songs = com.playlist.get_playlist_songs_id(playlists_id[i])
        playlists_songs.extend(playlist_songs)

    # 整合所有的歌
    all_songs_2 = []
    all_songs_2.extend(rank_songs)
    all_songs_2.extend(playlists_songs)

    # 去除列表中重复的歌
    all_songs = []
    for i in all_songs_2:
        if not i in all_songs:
            all_songs.append(i)
    print("正在提取用户最可能评论的歌曲信息...")

    # 多进程
    # 代理IP库初始化
    p1 = multiprocessing.Process(target=ProxiesDataBase.InitDB())
    p1.start()
    # 代理IP库刷新
    p2 = multiprocessing.Process(target=com.flash)
    p2.start()

    #进程池
    songs_sum = len(all_songs)
    pool=multiprocessing.Pool(processes=200)
    for i in range(len(all_songs)):
        print("======================================")
        print("正在爬取中... 当前第 " + str(i) + " 首,共计 " + str(songs_sum) + " 首")
        pool.apply_async(com.get_comments,(all_songs[i],))
        pool.apply_async(com.mysql_save)
    pool.close()
    pool.join()
    com.mysql_save()

"""
问题:
mysql user_num在删除之前的83个后，又从84开始而不是1开始
第一页url中total参数是true，后面页数url中total参数是false

[待解决]
在第500页之后（每页20），开始出现缺失，网页现象为重复几页

0
1
...
10014
10015
差 113081

123096
123097
...(共20条)
123114
123115

差 113081
236196
136197
...


"""
