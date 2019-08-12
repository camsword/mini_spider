#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: liangjie02
@file: mini_spider.py.py
@time: 2019-06-28 16:09
"""
import os
import sys
import argparse
import re
import configparser
from spider import log
from spider import crawl_thread
from spider import url_manager
from spider import result_queue
from spider import webpage_save
from spider import spider_config

logger = log.logger


def spider(config_path):
    """
    启动爬虫程序，根据配置文件进行爬取和停止
    :param config_path: 爬虫的配置文件路径
    :return:
    """
    # seedfile_path, result_path, max_depth, crawl_interval, \
    # crawl_timeout, thread_count, target_re = load_config(config_path)

    spider_config_obj = load_config(config_path)
    seedfile_path = spider_config_obj.seedfile
    result_path = spider_config_obj.result_path
    max_depth = spider_config_obj.max_depth
    crawl_interval = spider_config_obj.crawl_interval
    crawl_timeout = spider_config_obj.crawl_timeout
    thread_count = spider_config_obj.thread_count
    target_re = spider_config_obj.target_re

    target_re = re.compile(target_re)  # 编译正则对象
    seeds = load_seeds(seedfile_path)  # 获取种子列表

    # 构造Url管理器并且添加种子
    url_manager_obi = url_manager.UrlManager()
    if seeds and isinstance(seeds, list):
        url_manager_obi.add_new_urls(seeds)

    result_queue_obj = result_queue.ResultQueue()  # 保存结果的队列
    wb_save_thread = webpage_save.WebpageSave(result_queue_obj,
                                              result_path)  # 保存结果的线程

    # 添加爬虫线程并且启动
    crawl_threads = list()
    for index in range(thread_count):
        crawl_threads.append(crawl_thread.CrawlThread(url_manager_obi,
                                                      result_queue_obj,
                                                      crawl_interval,
                                                      crawl_timeout,
                                                      target_re,
                                                      "crawl_thread_%s" % index))

    for crawl_thread_obj in crawl_threads:
        crawl_thread_obj.start()  # 启动爬取线程

    wb_save_thread.start()  # 启动收集结果线程

    cur_depth = 0
    while True:
        logger.info("当前爬取深度：%d" % cur_depth)
        url_manager_obi.join()

        if cur_depth < max_depth:  # 添加所有线程新增的Url和符合预期的数据
            for crawl_thread_obj in crawl_threads:
                url_manager_obi.add_new_urls(crawl_thread_obj.get_new_urls())
                result_queue_obj.add_results(crawl_thread_obj.get_new_data())
                crawl_thread_obj.clear()
        elif cur_depth == max_depth:  # 只添加所有线程新增符合预期的数据,并且退出爬取线程
            for crawl_thread_obj in crawl_threads:
                result_queue_obj.add_results(crawl_thread_obj.get_new_data())
                crawl_thread_obj.clear()
                crawl_thread_obj.close()
            break
        cur_depth += 1  # 爬取结束后将深度加1

    result_queue_obj.join()
    wb_save_thread.close()  # 防止Queue的get方法阻塞，需要在get方法中添加超时时间和捕获异常s

    for crawl_thread_obj in crawl_threads:
        crawl_thread_obj.join()


def load_config(config_file):
    """
    获取爬虫配置文件信息
    :return: 返回配置信息的元祖(seedfile, result_path, max_depth, crawl_interval, crawl_timeout, thread_count, target_re)
    """
    if config_file and os.path.exists(config_file):
        config = configparser.ConfigParser()
        config.read(config_file)
        spider_section = "spider"
        try:
            if spider_section in config.sections():
                seedfile = config.get(spider_section, "seedfile")
                result_path = config.get(spider_section, "result")
                max_depth = config.getint(spider_section, "max_depth")
                crawl_interval = config.getint(spider_section, "crawl_interval")
                crawl_timeout = config.getint(spider_section, "crawl_timeout")
                thread_count = config.getint(spider_section, "thread_count")
                target_re = config.get(spider_section, "target_re")

                # return seedfile, result_path, max_depth, crawl_interval, crawl_timeout, thread_count, target_re
                return spider_config.SpiderConfig(seedfile,
                                                  result_path,
                                                  max_depth,
                                                  crawl_interval,
                                                  crawl_timeout,
                                                  thread_count,
                                                  target_re)
        except Exception as e:
            logger.error("读取配置文件出错，退出应用:%s" % e)
            sys.exit("读取配置文件出错，退出应用！")
    else:
        logger.error("配置文件路径无效，退出！")
        sys.exit("配置文件路径无效，退出！")


def load_seeds(seedfile):
    """
    获取种子
    :param seedfile:种子文件路径
    :return: 返回种子列表
    """
    if seedfile and os.path.exists(seedfile):
        with open(seedfile, 'r') as seedfile_obj:
            return seedfile_obj.readlines()


if __name__ == "__main__":
    desc = """根据-c选项提供的配置文件进行爬虫，并且保存符合特定规则的信息"""
    argparse_obj = argparse.ArgumentParser(prog="mini_spider",
                                           description=desc)
    argparse_obj.add_argument("-v",
                              "--version",
                              action="version",
                              version="%(prog)s 0.1",
                              help="显示版本信息")
    argparse_obj.add_argument("-c",
                              "--config",
                              required=True,
                              help="必填选项，输入爬虫配置文件路径")
    args = argparse_obj.parse_args()
    spider(args.config)
