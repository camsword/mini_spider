#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: liangjie02
@file: webpage_save.py
@time: 2019-06-30 10:01
"""
import os
import threading
import log

logger = log.logger


# logger = log.init_log("./log/mini_spider",
#                       "spider")


class WebpageSave(threading.Thread):
    """
    保存webpage中符合要求的数据的类
    """

    def __init__(self,
                 data_queue,
                 result_path,
                 thread_name="save_thread"):
        """
        初始化
        :param data_queue:爬虫数据的队列对象
        :param result_path:保存爬虫数据的文件路径
        :param name:线程的名字
        """
        super(WebpageSave, self).__init__(name=thread_name)
        self.data_queue = data_queue
        self.result_path = result_path
        self.stop_event = threading.Event()
        logger.info("初始化WebpageSave线程")

    def run(self):
        """
        启动线程，获取结果数据并且写入文件
        :return:
        """
        if self.result_path:
            if not os.path.exists(os.path.dirname(self.result_path)):
                os.makedirs(os.path.dirname(self.result_path), exist_ok=True)

        with open(self.result_path, 'w') as result_file:
            while not self.stop_event.is_set():
                data = self.data_queue.get_result()
                if data:
                    result_file.write(data + os.linesep)
                    # logger.info("写结果%s到文件" % data)
                    self.data_queue.task_done()

    def close(self):
        """
        结束线程
        :return:
        """
        self.stop_event.set()
