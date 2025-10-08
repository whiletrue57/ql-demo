#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set ts=4 sw=4 et:

import logging
import datetime
import os
import sys
import traceback
import requests

"""
任务名称
name: demo.py
定时规则
cron: * * * * *
"""

# ========================
# 飞书通知函数（从 FSKEY 获取 access_token）
# ========================
def send_feishu_alert(title: str, content: str):
    fskey = os.getenv("FSKEY")
    if not fskey:
        logging.warning("未配置 FSKEY 环境变量，跳过飞书通知")
        return False

    webhook_url = f"https://open.feishu.cn/open-apis/bot/v2/hook/{fskey}"

    payload = {
        "msg_type": "post",
        "post": {
            "zh_cn": {
                "title": title,
                "content": [
                    [
                        {"tag": "text", "text": content}
                    ]
                ]
            }
        }
    }

    try:
        resp = requests.post(webhook_url, json=payload, timeout=10)
        if resp.status_code == 200:
            logging.info("✅ 飞书告警发送成功")
            return True
        else:
            logging.error(f"❌ 飞书告警发送失败: {resp.status_code} - {resp.text}")
            return False
    except Exception as e:
        logging.error(f"❌ 发送飞书通知时发生异常: {e}")
        return False

# ========================
# 全局异常处理器
# ========================
def global_exception_handler(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    error_msg = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    script_name = os.path.basename(sys.argv[0])
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    title = "🚨 青龙任务执行失败"
    content = (
        f"**脚本名称**: `{script_name}`\n"
        f"**执行时间**: {current_time}\n"
        f"**传入参数**: `{' '.join(sys.argv[1:]) or '无'}`\n"
        f"**错误详情**:\n```\n{error_msg}\n```"
    )

    logging.error("💥 捕获到未处理异常，正在发送飞书告警...")
    send_feishu_alert(title, content)

# 安装全局异常钩子
sys.excepthook = global_exception_handler

# ========================
# 主程序
# ========================
def main():
    logging.info("Hello, World!")
    logging.info("This is a demo script.")
    logging.info("Current time: %s", datetime.datetime.now())
    logging.info("Arguments: %s", sys.argv)

    # 示例：触发 pandas 导入（如果未安装会报错并触发飞书通知）
    import pandas  # 如果报错，会被全局异常捕获

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    main()