# !/usr/bin/env python
# -*- coding: utf-8 -*-
import config
import base64
import requests
from Crypto.Cipher import AES
import json

"""
AES解密模块
    使用方式：
        get_json(url, param_type,total,offset,proxies)
        get_params(param_type,total,offset)      
        get_enSecKey()
        
    其中，param_type: comments，songs
         total: true or false
         offset : 默认 0

"""


# 获取Form Data中的parms（已两次加密）
def get_params(param_type, total, offset):
    param = config.get_first_param(param_type=param_type, total=total, offset=offset)
    h_encText = AES_encrypt(param, config.first_key, config.iv)
    h_encText = AES_encrypt(h_encText, config.second_key, config.iv)
    return h_encText


# 获取Form Data中的encSeckey（已配合param加密）
def get_encSecKey():
    return config.encSecKey


# 反向加密过程
def AES_encrypt(text, key, iv):
    pad = 16 - len(text) % 16
    text = text + pad * chr(pad)
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    encrypt_text = encryptor.encrypt(text)
    encrypt_text = str(base64.b64encode(encrypt_text))[2:-1]
    return encrypt_text


# 提交当前url的Form Data数据项
def get_json(url, param_type, total, offset, proxies):
    data = {
        "params": get_params(param_type=param_type, total=total, offset=offset),
        "encSecKey": get_encSecKey(),
    }
    response = requests.post(url, headers=config.user_headers, data=data, proxies=proxies)
    return response.content


if __name__ == "__main__":
    # 评论测试
    song_id = "656405"
    print("comments_test ===============================")
    print(json.loads(
        get_json(url=config.get_comments_url(song_id), param_type="comments", total=True, offset=0, proxies="")))

    # 排行榜测试
    print("rank_test ===============================")
    print(json.loads(get_json(url=config.url_rank, param_type="songs", total=True, offset=0, proxies="")))

    # 歌单测试
    print("playlist_test ===============================")
    print(json.loads(
        get_json(url=config.url_playlists, param_type="songs", total=True, offset=0, proxies="")))
