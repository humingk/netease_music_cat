# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------
import requests
from netease.form_data import form_data
import config
from my_tools.logger_tool import loggler_tool

logger = loggler_tool()


class request_data:
    """
    请求数据类

    """

    def get_request_data(self, first_param=None, url=None, proxies=None, api_type=config.api_weapi, eapi_url=None):
        """
        请求排行榜数据

        :param first_param: 参数
        :param url: 请求url
        :param proxies: 请求代理
        :param api_type: api类型
        :param eapi_url: eapi链接
        :return: status: 返回状态
        :return:response:请求数据
        """
        _form_data = None
        if first_param != "":
            _form_data = form_data().get_form_data(first_param=first_param, api_type=api_type, eapi_url=eapi_url)
        try:
            response = requests.post(url=url, headers=config.user_headers, data=_form_data, proxies=proxies).content
            status = True
            logger.debug("get_request_data success",
                         "url:{} ,first_param:{},proxies:{}".format(url, first_param, proxies))
        except Exception as e:
            response = None
            status = False
            logger.error("get_request_data failed",
                         "url:{} ,first_param:{},proxies:{},error_type:{},error:{}".format(url, first_param, proxies, type(e),e))
        return status, response


if __name__ == '__main__':
    r = request_data()
