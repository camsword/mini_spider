#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2018年7月9日

@author: liangjie02
"""
import os
import sys
import logging
import logging.handlers


def init_log(log_path,
             name=None,
             level=logging.INFO,
             when="D",
             backup=7,
             format="%(name)s:%(levelname)s:%(asctime)s:%(filename)s:%(lineno)d * %(thread)d %(message)s",
             datefmt="%m-%d %H:%M:%S"):
    """
    init_log - initialize log module

    Args:
    log_path:	Log file path prefix.
                Log data will go to two files: log_path.log and log_path.log.wf
                Any non-exist parent directories will be created automatically
    level:		msg above the level will be displayed
                DEBUG < INFO < WARNING < ERROR < CRITICAL
                the default value is logging.INFO
    when:		how to split the log file by time interval
                'S' : Seconds
                'M' : Minutes
                'H'	: Hours
                'D'	: Days
                'W'	: Week day
                default value: 'D'
    format:		format of the log
                default format : %(levelnames)s:%(asctime)s:%(filename)s:%(lineno)d * %(thread)d %(message)s
                INFO:06-24 16:00:11:log.py:40 * 122289898 hello word
    backup:		how many backup file to keep
                default value:7

    Raises:
    OSError: fail to create log directories
    IOError: fail to open log file
    """
    formatter = logging.Formatter(format, datefmt)
    logger = logging.getLogger(name)
    logger.setLevel(level)

    dir = os.path.dirname(log_path)
    if not os.path.isdir(dir):
        os.makedirs(dir)

    # 输出info以上的信息
    handler = logging.handlers.TimedRotatingFileHandler(filename=log_path + ".log",
                                                        when=when,
                                                        backupCount=backup)
    handler.setLevel(level)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # 只输出warning的信息
    handler = logging.handlers.TimedRotatingFileHandler(filename=log_path + ".log.wf",
                                                        when=when,
                                                        backupCount=backup)
    handler.setLevel(logging.WARNING)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # 标准输出流
    stdout_handler = logging.StreamHandler(stream=sys.stdout)
    stdout_handler.setLevel(level)
    stdout_handler.setFormatter(formatter)
    logger.addHandler(stdout_handler)

    return logger


logger = init_log("./log/mini_spider",
                  "spider")

if __name__ == "__main__":
    init_log("./log/mini_spider")
    logging.critical("test")
