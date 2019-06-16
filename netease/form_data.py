# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------
import config
import base64
from Crypto.Cipher import AES
from logger import loggler

log = loggler()


class form_data:
    """
    AES加密请求参数类
        利用fiddler分析网易云音乐中的core.js对请求表单参数的加密过程
        此模块模拟对请求表单参数的两次AES加密

    """

    def __get_params(self, first_param):
        """
        获取Form Data中的parms（通过两次AES加密）

        :param first_param: 第一个参数字典（由first_param获取）
        :return: 两次加密后的params
        """
        params = self.__AES_encrypt(first_param, config.first_key, config.iv)
        params = self.__AES_encrypt(params, config.second_key, config.iv)
        return params

    def __get_encSecKey(self):
        """
        获取Form Data中的encSeckey（已配合param加密）

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
        # 这里不能使用len(param),因为此处长度指标不能用中文，应该先转化为unicode
        pad = 16 - len(param.encode()) % 16
        param = param + pad * chr(pad)
        encryptor = AES.new(key, AES.MODE_CBC, iv)
        encrypt_text = encryptor.encrypt(param)
        encrypt_text = str(base64.b64encode(encrypt_text))[2:-1]
        return encrypt_text

    def get_form_data(self, first_param):
        form_data = {
            "params": self.__get_params(first_param),
            "encSecKey": self.__get_encSecKey()
        }
        return form_data


if __name__ == "__main__":
    d = form_data()
    print("comments_test ===============================")
    print(d.get_form_data("""{{rid:"{}",offset:"{}",total:"{}",limit:"{}",csrf_token:"{}"}}""" \
                          .format("", config.aes_offset, config.aes_total, config.aes_limit, "")))

    print("rank_test ===============================")
    print(d.get_form_data("""{{uid:"{}",offset:"{}",total:"{}",limit:"{}",type:"{}",csrf_token:"{}"}}""" \
                          .format(config.user_id, 0, config.aes_total, config.aes_limit, config.aes_ranklist_type, "")))
