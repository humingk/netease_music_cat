# !/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os
import random
import sys
import logging

"""
全局变量配置文件

"""

# 以下为自定义配置，请自行更改===============================================

# 用户信息
user_id = "474252223"
user_name = "IsolationTom"

# user_id="55494140"
# user_name="不散的和弦KC"

# 数据库信息 ----------------------------

# 数据库用户名
database_user_name = "root"

# 数据库用户密码
database_user_pwd = "1233"

# 数据库端口
database_port = 3306

# 数据库位置
database_host = "127.0.0.1"

# 数据库名称
database_name = "netease_music"

# 数据库编码方式
database_charset = "utf8mb4"

# 用户排行榜 ----------------------------
# 排行榜类型(请求表单参数，不可随意更改！)

# 最近一周
rank_type_week = 1
# 所有时间
rank_type_all = 0
# 最近一周+所有时间
rank_type_week_all = -1

# 默认排行榜类型
rank_type = 1

# 排行榜单中"最近一周"的最大歌曲选取数
week_rank_max = 100

# 排行榜单中"所有时间"的最大歌曲选取数
all_rank_max = 100

# 排行榜歌曲默认最大选取数
rank_max = all_rank_max

# 标准歌曲 ------------------------------

# 歌曲来源
song_source_default = 0
song_source_rank = 1
song_source_playlist = 2

# 标准歌曲默认类型
song_source_type = song_source_default

# 标准歌单 ------------------------------

# 歌单类型
normal_playlist = 4
default_playlist = 5
created_playlist = 6
collected_playlist = 7

# 标准歌单默认类型
playlist_type = 0

# 标准歌单最大歌曲选取数
playlist_songs_max = 50

# “用户喜欢的音乐”歌单 --------------------

# 是否爬取“用户喜欢的音乐”歌单
is_playlists_default = True

# “用户喜欢的音乐”歌单最大歌曲选取数
default_songs_max = sys.maxsize

# 用户创建的歌单 -------------------------

# 是否爬取用户创建的歌单
is_playlists_created = True

# 用户创建歌单的最大选取数
created_playlists_max = 20

# 用户创建歌单的歌曲最大选取数
created_songs_max = sys.maxsize

# 用户收藏的歌单 -------------------------

# 是否爬取用户收藏的歌单
is_playlists_collected = True

# 用户收藏歌单的最大选取数
collected_playlists_max = 10

# 用户收藏歌单的歌曲最大选取数
collected_songs_max = 20

# 歌曲评论 ------------------------------
# 每首歌的最大评论获取数(目前只能获取时间正序和时间倒序各10000条)
# 每首歌的最大评论获取数(目前只能获取时间正序和时间倒序各5000条)

# 最新评论最大
song_comments_new_max = 5000
# 最旧评论最大
song_comments_old_max = 5000
# 热门评论限制数(-1表示无限制)
song_comments_hot_max = -1

# 评论页数限制默认值
song_comments_page_limit = 100
# 抓取评论多线程默认个数
song_comments_thread_count = 20
# 给线程池添加任务的时间间隔(s)
song_comments_thread_thread_inteval_time = 1

# 评论类型
song_comments_type_default = 0
song_comments_type_hot = 1
song_comments_type = song_source_default

# 以下为基础配置，请勿更改=================================================

# 基本请求头
base_url = "http://music.163.com/"
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
host = "music.163.com"
language = "zh-CN,zh;q=0.9,en;q=0.8"
accept = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"

# 普通请求头
user_headers = {
    "User-Agent": user_agent,
    "Host": host,
    "Accept": accept,
    "Referer": base_url,
    "Accept-Language": language
}

# 为eapi添加的请求头
user_headers_eapi = {
    'os': 'osx',
    'appver': '2.5.3',
    # 'requestId': str(random.randint(10000000, 99999999)),
    'requestId': 66178368,
    'clientSign': '',
}

# eapi的请求参数（eapi公共）
eapi_params = {
    'verifyId': 1,
    'os': 'OSX',
    'header': json.dumps(user_headers_eapi, separators=(',', ':'))
}

# 用于测试的歌曲id
song_id = "656405"

# 用于测试的歌单id
playlist_id = "13928655"

# 日志信息
logger_name = "logger"
logger_file = "default"
project_root = os.path.dirname(__file__)
logger_path = project_root + "/logger.log"
logger_formatter = "%(asctime)s %(levelname)s %(message)s"
logger_console_level = logging.DEBUG
logger_file_level = logging.DEBUG

# AES加密模块 ================================================================

"""
1. 只有 first_param 需由不同的加密类型确定，其他参数均可固定
2. second_key 和 encSecKey 可任意但需要相对保持不变

"""

# total参数默认值
aes_total = True

# offset参数默认值
aes_offset = 0

# limit限制默认值
aes_limit = 1000

# 用户排行榜类型默认值(暂时未知用途)
aes_ranklist_type = -1

# 搜索 ----------------------------
# 搜索单曲
search_type_song = 1
# 搜索专辑
search_type_album = 10
# 搜索歌手
search_type_artist = 100
# 搜索歌单
search_type_playlist = 1000
# 搜索用户
search_type_user = 1002
# 搜索mv
search_type_mv = 1004
# 搜索歌词
search_type_lyric = 1006
# 搜索电台
search_type_radio = 1009
# 搜索视频
search_type_video = 1014

# 搜索表单类型默认值
search_type = search_type_song

# 四个请求参数 -------------------------------

# 第一个参数类型（在first_param中获取）

# 请求格式错误
aes_param_error = -1
# 请求评论
aes_param_comment = 1
# 请求用户排行榜
aes_param_ranklist = 2
# 请求搜索
aes_param_search = 3

# 默认请求类型
aes_first_param_type = aes_param_error

# api类型
api_weapi = 0
api_eapi = 1
api_type = api_weapi

second_param = "010001"
third_param = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
forth_param = "0CoJUm6Qyw8W8jud"

# eapikey
eapikey = "e82ckenh8dichen8"

# 用于获取params的两次AES加密Key
first_key = forth_param
second_key = 16 * 'F'

# 密钥偏移量
iv = "0102030405060708"

# encSecKey
encSecKey = "257348aecb5e556c066de214e531faadd1c55d814f9be95fd06d6bff9f4c7a41f831f6394d5a3fd2e3881736d94a02ca919d952872e7d0a50ebfa1769a7a62d512f5f1ca21aec60bc3819a9c3ffca5eca9a0dba6d6f7249b06f5965ecfff3695b54e1c28f3f624750ed39e7de08fc8493242e26dbc4484a01c76f739e135637c"

# url ================================================================

# 用户排行榜url
url_user_rank = "https://music.163.com/weapi/v1/play/record"

# 用户主页歌单url
url_user_playlists = "https://music.163.com/weapi/user/playlist"

# 歌单url
url_playlist = "https://music.163.com/weapi/v3/playlist/detail"

# 搜索url
url_search = "https://music.163.com/weapi/search/get"


def get_playlist_url(playlist_id):
    """
    歌单url + 歌单id
    :param playlist_id: 歌单id
    :return: 歌单url
    """
    return "https://music.163.com/playlist?id={}".format(playlist_id)


def get_comments_url(song_id):
    """
    歌曲评论url+歌曲id

    :param song_id: 歌曲id
    :return: 歌曲评论url
    """
    return "http://music.163.com/weapi/v1/resource/comments/R_SO_4_{}".format(song_id)


def get_comments_default_url(song_id):
    """
    歌曲普通评论
    url+歌曲id

    :param song_id: 歌曲id
    :return: 歌曲评论url
    """
    return "http://music.163.com/eapi/v1/resource/comments/R_SO_4_{}".format(song_id)


def get_comment_default_url_for_eapi_param(song_id):
    """
    歌曲普通评论
    eapi的param中url取值

    :param song_id: 歌曲id
    :return:
    """
    return "/api/v1/resource/comments/R_SO_4_{}".format(song_id)


def get_comments_hot_url(song_id):
    """
    歌曲热门评论
    url+歌曲id

    :param song_id: 歌曲id
    :return: 歌曲评论url
    """
    return "http://music.163.com/eapi/v1/resource/hotcomments/R_SO_4_{}".format(song_id)


def get_comment_hot_url_for_eapi_param(song_id):
    """
    歌曲热门评论
    eapi的param中url取值

    :param song_id: 歌曲id
    :return:
    """
    return "/api/v1/resource/hotcomments/R_SO_4_{}".format(song_id)
