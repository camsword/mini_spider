#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: liangjie02
@file: url_downloador.py
@time: 2019-06-30 07:56
"""
import requests
import log

logger = log.logger


# logger = log.init_log("./log/mini_spider",
#                       "spider")


class WebpageDownloador(object):
    """
    Url下载器
    """

    def __init__(self,
                 timeout):
        """
        初始化UrlDownloador
        :param timeout: 爬虫超时时间
        """
        self.timeout = timeout

    def download(self,
                 url):
        """
        :param url: 下载的Url
        :return: 返回url对应的网页内容
        """
        try:
            resp = requests.get(url,
                                timeout=self.timeout)

            if resp and resp.status_code == requests.codes.ok:
                return resp.text
        except Exception as e:
            logger.error("访问Url出错:%s" % e)

