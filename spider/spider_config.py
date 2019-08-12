#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: liangjie02
@file: spider_config.py
@time: 2019-08-09 15:37
"""


class SpiderConfig(object):
    """
    爬虫配置信息类
    """

    def __init__(self,
                 seedfile,
                 result_path,
                 max_depth,
                 crawl_interval,
                 crawl_timeout,
                 thread_count,
                 target_re):
        """
        配置类初始化
        :param seedfile: 种子文件
        :param result_path: 结果路径
        :param max_depth: 爬取深度
        :param crawl_interval: 爬取间隔
        :param crawl_timeout: 超时
        :param thread_count: 爬取线程数
        :param target_re: 爬取目标正则表达式
        """
        self.seedfile = seedfile
        self.result_path = result_path
        self.max_depth = max_depth
        self.crawl_interval = crawl_interval
        self.crawl_timeout = crawl_timeout
        self.thread_count = thread_count
        self.target_re = target_re