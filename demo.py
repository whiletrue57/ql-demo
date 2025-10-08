#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 🔥 必须放在第一行（在任何可能出错的 import 之前）
import traceback_alert

# 从这里开始，所有未处理异常都会被自动捕获并告警
import logging
import datetime
import sys
# import pandas  # 即使这里报错，也会触发飞书通知！
# a = 1 / 0  # 故意制造一个错误，测试全局异常处理器
# a = 1 + "1"


"""
任务名称
name: demo.py
定时规则
cron: * * * * *
"""

def main():
    logging.info("Hello, World!")
    logging.info("This is a demo script.")
    logging.info("Current time: %s", datetime.datetime.now())
    logging.info("Arguments: %s", sys.argv)

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    main()