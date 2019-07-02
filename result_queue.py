#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: liangjie02
@file: result_queue.py
@time: 2019-06-30 12:28
"""
import queue
import log

logger = log.logger


# logger = log.init_log("./log/mini_spider",
#                       "spider")


class ResultQueue(object):
    """
    保存爬取到的数据到队列
    """

    def __init__(self):
        """
        初始化
        :param
        """
        self.result_queue = queue.Queue()  # 保存结果的队列

    def add_results(self,
                    result_list):
        """
        添加结果文件到Queue中
        :param result_list: 添加的结果数据列表
        :return:
        """
        if isinstance(result_list, list) and result_list:
            for result in result_list:
                # logger.info("添加结果数据:%s" % result)
                self.result_queue.put(result)

    def get_result(self):
        """
        从结果队列中获取一个结果数据
        :return:
        """
        try:
            return self.result_queue.get(timeout=5)
        except Exception as e:
            logger.warn("队列中暂无待获取的结果")

    def task_done(self):
        self.result_queue.task_done()

    def join(self):
        self.result_queue.join()
