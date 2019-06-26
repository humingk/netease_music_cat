# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------
import hashlib
from binascii import b2a_hex
import config
import base64
from Crypto.Cipher import AES
from my_tools.logger_tool import loggler_tool

logger = loggler_tool()


class form_data:
    """
    AES加密请求参数类
        利用fiddler分析网易云音乐中的core.js对请求表单参数的加密过程
        此模块模拟对请求表单参数的两次AES加密

    """

    def __get_weapi_params(self, first_param):
        """
        获取weapi Form Data中的parms（通过两次AES加密）

        :param first_param: 第一个参数字典（由first_param获取）
        :return: 两次加密后的params
        """
        params = self.__AES_encrypt(mode=AES.MODE_CBC, param=first_param, key=config.first_key, iv=config.iv)
        params = str(base64.b64encode(params))[2:-1]
        params = self.__AES_encrypt(mode=AES.MODE_CBC, param=params, key=config.second_key, iv=config.iv)
        return str(base64.b64encode(params))[2:-1]

    def __get_eapi_params(self, eapi_url, first_param):
        """
        获取eapi Form Data中的params(通过一次AES加密)

        :param eapi_url: 请求url 字符串
        :param first_param:  第一个参数字典 字符串
        :return: 一次加密后的params
        """
        first_param = first_param.encode()
        eapi_url = eapi_url.encode()
        params = b'nobody' + eapi_url + b'use' + first_param + b'md5forencrypt'
        md5 = hashlib.md5()
        md5.update(params)
        params = eapi_url + b'-36cd479b6b5-' + first_param + b'-36cd479b6b5-' + md5.hexdigest().encode()
        pad = 16 - len(params) % 16
        params = params + bytearray([pad] * pad)
        crypt = AES.new(config.eapikey, AES.MODE_ECB)
        params = crypt.encrypt(params)
        return b2a_hex(params).upper()

    def __get_encSecKey(self):
        """
        获取Form Data中的encSeckey（已配合param加密）

        :return: encSecKey
        """
        return config.encSecKey

    def __AES_encrypt(self, mode, param, key, iv):
        """
        AES加密过程

        :param mode: AES模式
        :param param: AES加密对象
        :param key: AES加密秘钥
        :param iv: AES秘钥偏移量
        :return: AES加密结果
        """
        # 这里不能使用len(param),因为此处长度指标不能用中文，应该先转化为unicode
        pad = 16 - len(param.encode()) % 16
        param = param + pad * chr(pad)
        encryptor = AES.new(key, mode, iv)
        encrypt_text = encryptor.encrypt(param)
        return encrypt_text

    def get_form_data(self, first_param, api_type=config.api_weapi, eapi_url=None):
        """
        获取请求参数

        :param first_param: 第一个请求字典
        :param api_type: api类型
        :param eapi_url: eapi的请求链接
        :return:
        """
        if api_type == config.api_weapi:
            return {
                "params": self.__get_weapi_params(first_param),
                "encSecKey": self.__get_encSecKey()
            }
        elif api_type == config.api_eapi:
            return {
                "params": self.__get_eapi_params(eapi_url=eapi_url, first_param=first_param)
            }
        else:
            return None


if __name__ == "__main__":
    d = form_data()
    print("comments_test ===============================")
    print(d.get_form_data("""{{rid:"{}",offset:"{}",total:"{}",limit:"{}",csrf_token:"{}"}}""" \
                          .format("", config.aes_offset, config.aes_total, config.aes_limit, "")))

    print("rank_test ===============================")
    print(d.get_form_data("""{{uid:"{}",offset:"{}",total:"{}",limit:"{}",type:"{}",csrf_token:"{}"}}""" \
                          .format(config.user_id, 0, config.aes_total, config.aes_limit, config.aes_ranklist_type, "")))
