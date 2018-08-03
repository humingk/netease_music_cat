# !/usr/bin/env python
# -*- coding: utf-8 -*-
import config
import base64
import requests
from Crypto.Cipher import AES
import json

"""
解密过程部分参考:
https://www.zhihu.com/question/36081767/answer/140287795
from 知乎 平胸小仙女

"""

user_cookie = config.user_cookie

# 根据core.js找到四个加密参数param
first_param = config.first_param
second_param = config.second_param
third_param = config.third_param
forth_param = config.forth_param

base_url = config.base_url
user_agent = config.user_agent
language = config.language
url_referer = base_url

# 请求头
user_headers = {
    "User-Agent": user_agent,
    "Cookie": user_cookie,
    "Referer": url_referer,
    "Accept-Language": language
}

proxies = ""


# 获取第page页Form Data中的parms数据项（已加密）
def get_params(param):
    iv = "0102030405060708"
    first_key = forth_param
    second_key = 16 * 'F'
    h_encText = AES_encrypt(param, first_key, iv)
    h_encText = AES_encrypt(h_encText, second_key, iv)
    return h_encText


# 获取第page页Form Data中的encSeckey数据项（已加密）
def get_encSecKey():
    encSecKey = "257348aecb5e556c066de214e531faadd1c55d814f9be95fd06d6bff9f4c7a41f831f6394d5a3fd2e3881736d94a02ca919d952872e7d0a50ebfa1769a7a62d512f5f1ca21aec60bc3819a9c3ffca5eca9a0dba6d6f7249b06f5965ecfff3695b54e1c28f3f624750ed39e7de08fc8493242e26dbc4484a01c76f739e135637c"
    return encSecKey


# 反向加密过程
def AES_encrypt(text, key, iv):
    pad = 16 - len(text) % 16
    text = text + pad * chr(pad)
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    encrypt_text = encryptor.encrypt(text)
    encrypt_text = str(base64.b64encode(encrypt_text))[2:-1]
    return encrypt_text


# 提交当前（第page页面）的Form Data数据项
def get_json(url, params, encSecKey, proxies):
    data = {
        "params": params,
        "encSecKey": encSecKey,
    }
    response = requests.post(url, headers=user_headers, data=data, proxies=proxies)
    return response.content


# 控制台测试
if __name__ == "__main__":
    params_obj = get_params(first_param)
    encSecKey_obj = get_encSecKey()

    song_id = "1919749"
    url = "http://music.163.com/weapi/v1/resource/comments/R_SO_4_" + song_id + "?csrf_token="

    json_text = get_json(url, params_obj, encSecKey_obj)
    json_obj = json.loads(json_text)
    print(json_obj)
