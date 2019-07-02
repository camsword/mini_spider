#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: liangjie02
@file: url_manager.py
@time: 2019-06-30 07:55
"""

import queue
from spider import log

logger = log.logger


# logger = log.init_log("./log/mini_spider",
#                       "spider")


class UrlManager(object):
    """
    Url管理器，针对将要爬虫或已经爬虫过的Url进行管理
    """

    def __init__(self):
        """
        初始化一个Queue存放将要爬虫的Url
        一个Set存放已经爬过的Url，用来去重操作
        """
        self.new_url_queue = queue.Queue()
        self.all_url_set = set()

    def add_new_url(self, url):
        """
        添加一个新的Url
        :param url: 要被爬虫的新的Url
        :return:
        """

        if url and url not in self.all_url_set:
            self.all_url_set.add(url)
            self.new_url_queue.put(url)
            # logger.info("添加url:%s" % url)

    def add_new_urls(self, urls):
        """
        添加一个Url集合
        :param urls: Url集合
        :return:
        """
        if isinstance(urls, list):
            for url_item in urls:
                self.add_new_url(url_item)
        logger.info("剩余Urls个数:%d" % self.new_url_queue.qsize())
        logger.info("已经爬虫过的Url:%d" % (len(self.all_url_set) - self.new_url_queue.qsize()))

    def get_url(self):
        """
        获取一个Url并且返回
        :return:
        """
        try:
            return self.new_url_queue.get(timeout=5)
        except Exception as e:
            logger.warn("队列中暂无待爬取的url")

    def task_down(self):
        """
        一个Url爬取结束后通知Queue
        :return:
        """
        self.new_url_queue.task_done()

    def join(self):
        """
        阻塞调用线程，直到所有的任务被处理完成
        :return:
        """
        self.new_url_queue.join()

    def is_empty(self):
        """
        查看队列中的Url是否已经为空
        :return:
        """
        return self.new_url_queue.empty()
