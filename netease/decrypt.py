# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------
import config
import base64
import requests
from Crypto.Cipher import AES
import json
import logger

log = logger.loggler()


class decrypt:
    """
    AES加密及提交请求类
        利用fiddler分析网易云音乐中的core.js对请求表单参数的加密过程
        此模块模拟对请求表单参数的两次AES加密，并提交请求表单

    """

    def __get_params(self, user_id, param_type, total, offset):
        """
        获取Form Data中的第一个参数 parms（两次加密）

        :param user_id: 用户id，若type为comment，user_id可为空
        :param param_type: 需要加密的类型，eg:comments,songs
        :param total: 请求表单参数，详见config
        :param offset: 请求表单参数，详见config
        :return: 两次加密后的params
        """
        first_param = config.get_first_param(user_id=user_id, param_type=param_type, total=total, offset=offset)
        params = self.__AES_encrypt(first_param, config.first_key, config.iv)
        params = self.__AES_encrypt(params, config.second_key, config.iv)
        return params

    def __get_encSecKey(self):
        """
        获取Form Data中的第二个参数 encSeckey（已配合指定param加密）

        :return: encSecKey
        """
        return config.encSecKey

    def __AES_encrypt(self, param, key, iv):
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

    def get_json(self, user_id, url, param_type, total, offset, proxies):
        """
        post提交当前url的Form Data数据项

        :param user_id: 用户id，若type为comment，user_id可为空
        :param url: post请求url
        :param param_type: 需要加密的类型，eg:comments,songs
        :param total: 请求表单参数，详见config
        :param offset: 请求表单参数，详见config
        :param proxies: 代理
        :return: status: 是否成功获取
        :return: 返回结果
        """
        data = {
            "params": self.__get_params(user_id=user_id, param_type=param_type, total=total, offset=offset),
            "encSecKey": self.__get_encSecKey(),
        }
        try:
            response = requests.post(url, headers=config.user_headers, data=data, proxies=proxies)
            status=True
            log.debug("decrypt get_json",
                      "get response success by decrypt user:{} param-type:{} offset:{}".format(user_id, param_type,
                                                                                               offset))
        except Exception as e:
            response = None
            status=False
            log.error("decrypt get_json",
                      "get response failed by decrypt user:{} param-type:{} offset:{} :{}".format(user_id, param_type,
                                                                                                  offset, e))

        return status,response.content


if __name__ == "__main__":
    d = decrypt()
    print("comments_test ===============================")
    print(json.loads(
        d.get_json(user_id=None, url=config.get_comments_url(config.song_id), param_type="comments", total=True,
                   offset=0,
                   proxies="")[1]))

    print("rank_test ===============================")
    print(json.loads(
        d.get_json(user_id=config.user_id, url=config.url_rank, param_type="songs", total=True, offset=0, proxies="")[1]))

    print("playlist_test ===============================")
    print(json.loads(
        d.get_json(user_id=config.user_id, url=config.url_playlists, param_type="songs", total=True, offset=0,
                   proxies="")[1]))
