# !/usr/bin/env python
# -*- coding: utf-8 -*-
import config
import base64
import requests
from Crypto.Cipher import AES
import json

"""
AES加密及提交请求模块
    利用fiddler分析网易云音乐中的core.js对请求表单参数的加密过程
    此模块模拟对请求表单参数的两次AES加密，并提交请求表单

"""


def __get_params(user_id, param_type, total, offset):
    """
    获取Form Data中的第一个参数 parms（两次加密）

    :param user_id: 用户id，若type为comment，user_id可为空
    :param param_type: 需要加密的类型，eg:comments,songs
    :param total: 请求表单参数，详见config
    :param offset: 请求表单参数，详见config
    :return: 两次加密后的params
    """
    first_param = config.get_first_param(user_id=user_id, param_type=param_type, total=total, offset=offset)
    params = __AES_encrypt(first_param, config.first_key, config.iv)
    params = __AES_encrypt(params, config.second_key, config.iv)
    return params


def __get_encSecKey():
    """
    获取Form Data中的第二个参数 encSeckey（已配合指定param加密）

    :return: encSecKey
    """
    return config.encSecKey


def __AES_encrypt(param, key, iv):
    """
    AES加密过程

    :param param: AES加密对象
    :param key: AES加密秘钥
    :param iv: AES秘钥偏移量
    :return: AES加密结果
    """

    pad = 16 - len(param) % 16
    param = param + pad * chr(pad)
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    encrypt_text = encryptor.encrypt(param)
    encrypt_text = str(base64.b64encode(encrypt_text))[2:-1]
    return encrypt_text


def get_json(user_id, url, param_type, total, offset, proxies):
    """
    post提交当前url的Form Data数据项

    :param user_id: 用户id，若type为comment，user_id可为空
    :param url: post请求url
    :param param_type: 需要加密的类型，eg:comments,songs
    :param total: 请求表单参数，详见config
    :param offset: 请求表单参数，详见config
    :param proxies: 代理
    :return: post返回结果
    """
    data = {
        "params": __get_params(user_id=user_id, param_type=param_type, total=total, offset=offset),
        "encSecKey": __get_encSecKey(),
    }
    response = requests.post(url, headers=config.user_headers, data=data, proxies=proxies)
    return response.content


if __name__ == "__main__":
    print("comments_test ===============================")
    print(json.loads(
        get_json(user_id=None, url=config.get_comments_url(config.song_id), param_type="comments", total=True, offset=0,
                 proxies="")))

    print("rank_test ===============================")
    print(json.loads(
        get_json(user_id=config.user_id, url=config.url_rank, param_type="songs", total=True, offset=0, proxies="")))

    print("playlist_test ===============================")
    print(json.loads(
        get_json(user_id=config.user_id, url=config.url_playlists, param_type="songs", total=True, offset=0,
                 proxies="")))
