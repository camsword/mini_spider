#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: liangjie02
@file: url_parse.py
@time: 2019-06-30 07:55
"""
from urllib import parse as url_parse
import bs4
from spider import log

logger = log.logger


class WebpageParse(object):
    """
    针对webpage页面的内容进行解析的类
    """

    def parse(self,
              cur_url,
              webpage,
              target_re):
        """
        获取符合正则表达式url_re的Url和data_re的数据
        :param cur_url: 当前页面的url
        :param webpage: 被解析的web页面内容
        :param target_re: 匹配数据的正则表达式
        :return: 符合url_re的list和data_re的数据
        """
        urls = []
        data = []
        if webpage:
            soup = bs4.BeautifulSoup(webpage,
                                     "html.parser",
                                     from_encoding="utf-8")
            urls = self.__get_urls(cur_url,
                                   soup)
            data = self.__get_data(cur_url,
                                   webpage,
                                   target_re)
            if urls:
                logger.info("获取到新的爬虫Url个数:%s" % len(urls))
            if data:
                logger.info("获取到符合要求的数据个数:%s" % len(data))
        return urls, data

    def __get_urls(self,
                   cur_url,
                   soup):
        urls = list()
        links = soup.find_all("a", href=True)
        for link in links:
            href_url = link.get("href")
            if href_url.startswith("http"):
                urls.append(href_url)
            elif "javascript:location.href" in href_url:
                urls.append(url_parse.urljoin(cur_url,
                                              href_url.split("=")[-1].split("\"")[-2]))
            else:
                urls.append(url_parse.urljoin(cur_url,
                                              href_url))
        return urls

    def __get_data(self,
                   cur_url,
                   webpage,
                   target_re):
        data = list()
        # images = soup.find_all("img", src=True)
        all_targets = target_re.findall(webpage)
        for target in all_targets:
            # target = target.get("src")
            if target.startswith("http"):
                data.append(target)
            else:
                data.append(url_parse.urljoin(cur_url,
                                              target))
        return data
