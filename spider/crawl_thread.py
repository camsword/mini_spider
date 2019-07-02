#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: liangjie02
@file: crawl_thread.py.py
@time: 2019-06-30 10:00
"""
import time
import threading
from spider import webpage_downloador
from spider import webpage_parse
from spider import log

logger = log.logger


# logger = log.init_log("./log/mini_spider",
#                       "spider")


class CrawlThread(threading.Thread):
    """
    爬虫线程，用来爬取数据并且存储爬取后的结果、以及新的Url
    """

    def __init__(self,
                 url_manager,
                 result_queue,
                 crawl_interval,
                 crawl_timeout,
                 target_re,
                 thread_name="crawl_thread"):
        super(CrawlThread, self).__init__(name=thread_name)
        self.url_manager = url_manager
        self.result_queue = result_queue
        self.crawl_interval = crawl_interval
        self.crawl_timeout = crawl_timeout
        # self.url_re = url_re
        self.target_re = target_re
        self.close_event = threading.Event()  # 当符合特定条件的情况下停止线程
        self.new_urls = list()
        self.new_data = list()

    def run(self):
        """
        爬取Url和获取匹配的Url和结果数据
        :return:
        """

        wp_downloador = webpage_downloador.WebpageDownloador(self.crawl_timeout)
        wp_parse = webpage_parse.WebpageParse()

        while not self.close_event.is_set():
            crawl_url = self.url_manager.get_url()  # 获取一个url开始进行爬虫
            if crawl_url:
                logger.info("开始抓取url:%s" % crawl_url)

                webpage_content = wp_downloador.download(crawl_url)
                urls, result_list = wp_parse.parse(crawl_url,
                                                   webpage_content,
                                                   self.target_re)

                self.new_urls.extend(urls)  # 保存符合条件的url
                self.new_data.extend(result_list)
                # self.result_queue.add_results(result_list)  # 将结果文件添加到队列中

                self.url_manager.task_down()  # 任务结束后告诉url_manager移除已经完成元素
            time.sleep(self.crawl_interval)  # 暂停crawl_interval间隔

    def get_new_urls(self):
        """
        获取该线程爬取的新的Url列表
        :return: 返回新增需要爬虫的Url列表
        """
        return self.new_urls

    def clear(self):
        """
        清理上次保存的数据结果，只有在合适的时间调用
        :return:
        """
        self.new_urls.clear()
        self.new_data.clear()

    def get_new_data(self):
        """
        获取本深度爬取的结果数据
        :return: 返回新增符合预期的数据列表
        """
        return self.new_data

    def close(self):
        """
        退出子线程
        :return:
        """
        self.close_event.set()
