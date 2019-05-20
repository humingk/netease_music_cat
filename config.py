# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
全局变量配置文件

"""

# 以下为自定义配置，请自行更改=================================

# 1. 更改为需要爬取的用户ID (用户首页URL中的ID)
user_id = "55494140"

# 2. 更改为自己数据库的用户名
database_user_name = "root"

# 3. 更改为自己数据库的用户密码
database_user_pwd = "1233"

# 4. 排行榜单中最近一周的最大歌曲选取数
# 选取数越大，可获取的评论范围越广，但更加耗费资源，且准确度与选取数成log关系，不建议过大
rank_week_max = 50

# 5. 排行榜单中所有时间的最大歌曲选取数
# 同上
rank_all_max = 100

# 6. 用户歌单列表的最大歌单选取数(包含用户创建、收藏的歌单)
# 同上
playlists_max = 10

# 7.用户歌单中最大歌曲选取数(不包含用户喜欢的音乐歌单)
# 同上
playlist_songs_max = 20

# 8. 是否只爬取用户自己创建的歌单？
# 默认否(False),若歌单较多可选择True
only_playlists_created = False

# 9. 每首歌的最大评论获取数(目前最多只能获取时间正序的10000条和时间倒序的10000条)
# 时间 最新评论
song_comments_new_max = 10000
# 时间 最旧评论
song_comments_old_max = 10000

# 以下为基础配置，请勿更改==========================

# 数据库信息
database_name = "music"
database_charset = "utf8mb4"
table_user_name = "users"
table_user_cols_temp = {
    "user_name": "",
    "user_id": "",
    "comment_id": ""
}
table_user_cols = ",".join(table_user_cols_temp.keys())
table_comment_name = "comments"
table_comment_cols_temp = {
    "comment_id": "",
    "comment_song_name": "",
    "comment_content": "",
    "comment_time": ""
}
table_comment_cols = ",".join(table_comment_cols_temp.keys())

# 基本请求头
base_url = "http://music.163.com/"
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
host = "music.163.com"
language = "zh-CN,zh;q=0.9,en;q=0.8"
accept = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"

user_headers = {
    "User-Agent": user_agent,
    "Host": host,
    "Accept": accept,
    "Referer": base_url,
    "Accept-Language": language
}

# 当前页评论页数
page_offset = "0"

# 评论页数限制
page_limit = "100"

# AES 解密模块
"""
1. 只有 first_param 需由不同的加密类型确定，其他参数均可固定
2. second_key 和 encSecKey 可任意但需要相对保持不变

"""


# 根据core.js找到四个加密参数param
# 第一个param参数,由加密类型决定
# total: true or false
# offset: 默认0
def get_first_param(param_type, total, offset):
    if param_type == "comments":
        print("{rid:\"\", offset:" + str(offset) + ", total:\"" + str(total) + "\", limit:" + str(
            page_limit) + ", csrf_token:\"\"}")
        return "{rid:\"\", offset:" + str(offset) + ", total:\"" + str(total) + "\", limit:" + str(
            page_limit) + ", csrf_token:\"\"}"
    elif param_type == "songs":
        return "{uid:\"" + str(user_id) + "\",type:\"-1\",limit:\"1000\",offset:" + str(offset) + ",total:\"" + str(
            total) + "\",csrf_token:\"\"}"


second_param = "010001"
third_param = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
forth_param = "0CoJUm6Qyw8W8jud"

# 用于获取params的两次AES加密Key
first_key = forth_param
second_key = 16 * 'F'

# 密钥偏移量
iv = "0102030405060708"

# encSecKey
encSecKey = "257348aecb5e556c066de214e531faadd1c55d814f9be95fd06d6bff9f4c7a41f831f6394d5a3fd2e3881736d94a02ca919d952872e7d0a50ebfa1769a7a62d512f5f1ca21aec60bc3819a9c3ffca5eca9a0dba6d6f7249b06f5965ecfff3695b54e1c28f3f624750ed39e7de08fc8493242e26dbc4484a01c76f739e135637c"

# 排行榜url
url_rank = 'http://music.163.com/weapi/v1/play/record?csrf_token='

# 主页歌单url
url_playlists = "https://music.163.com/weapi/user/playlist?csrf_token="


# 歌单url + 歌单id
def get_playlist_url(playlist_id):
    return "https://music.163.com/playlist?id=" + str(playlist_id)


# 歌曲评论url
def get_comments_url(song_id):
    return "http://music.163.com/weapi/v1/resource/comments/R_SO_4_" + str(song_id) + "?csrf_token="
