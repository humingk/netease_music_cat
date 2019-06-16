# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------
import requests
from netease.form_data import form_data
import config
from logger import loggler

log = loggler()


class request_data:
    """
    请求数据类

    """

    def get_request_data(self, first_param="", url="", proxies=""):
        """
        请求排行榜数据

        :param first_param: 参数
        :param url: 请求url
        :param proxies: 请求代理
        :return: status: 返回状态
        :return:response:请求数据
        """
        _form_data = None
        if first_param != "":
            _form_data = form_data().get_form_data(first_param=first_param)
        try:
            response = requests.post(url=url, headers=config.user_headers, data=_form_data, proxies=proxies).content
            status = True
            log.debug("get_request_data success",
                      "url:{} ,first_param:{},proxies:{}".format(url, first_param, proxies))
        except Exception as e:
            response = None
            status = False
            log.error("get_request_data failed",
                      "url:{} ,first_param:{},proxies:{},error:{}".format(url, first_param, proxies, e))
        return status, response


if __name__ == '__main__':
    r = request_data()
