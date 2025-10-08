# traceback_alert.py
import os
import sys
import traceback
import datetime

# 尝试导入 requests，失败则用 urllib（确保告警本身不因依赖缺失而失效）
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False
    import urllib.request
    import urllib.parse
    import json

def _send_feishu_alert(title: str, content: str):
    fskey = os.getenv("FSKEY")
    if not fskey:
        print("[告警] 未配置 FSKEY，跳过飞书通知", file=sys.stderr)
        return False

    webhook_url = f"https://open.feishu.cn/open-apis/bot/v2/hook/{fskey}"
    # ✅ 改为 text 类型（纯文本）
    full_message = f"{title}\n\n{content}"
    payload = {
        "msg_type": "text",
        "content": {
            "text": full_message
        }
    }

    try:
        if HAS_REQUESTS:
            resp = requests.post(webhook_url, json=payload, timeout=10)
            success = resp.status_code == 200
        else:
            data = json.dumps(payload).encode('utf-8')
            req = urllib.request.Request(webhook_url, data=data, headers={'Content-Type': 'application/json'})
            with urllib.request.urlopen(req, timeout=10) as f:
                resp_data = f.read().decode()
            success = '"StatusCode":0' in resp_data or '"code":0' in resp_data

        if success:
            print("[告警] 飞书通知发送成功", file=sys.stderr)
            return True
        else:
            print(f"[告警] 飞书发送失败", file=sys.stderr)
            return False
    except Exception as e:
        print(f"[告警] 发送异常: {e}", file=sys.stderr)
        return False

def _global_exception_handler(exc_type, exc_value, exc_traceback):
    # 忽略 KeyboardInterrupt (Ctrl+C)
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    # 1. 输出原始错误到 stderr（青龙日志可见）
    print("\n" + "="*60, file=sys.stderr)
    print("💥 程序发生未处理异常，原始错误堆栈如下:", file=sys.stderr)
    traceback.print_exception(exc_type, exc_value, exc_traceback, file=sys.stderr)
    print("="*60 + "\n", file=sys.stderr)

    # 2. 发送飞书告警
    error_msg = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    script_name = os.path.basename(sys.argv[0])
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    title = "🚨 青龙任务执行失败"
    content = (
        f"脚本名称: {script_name}\n"
        f"执行时间: {current_time}\n"
        f"传入参数: {' '.join(sys.argv[1:]) or '无'}\n"
        f"错误详情:\n{error_msg}"
    )

    _send_feishu_alert(title, content)

# 🔥 自动安装全局异常钩子！
sys.excepthook = _global_exception_handler

# 可选：提供手动调用接口（用于主动上报）
def report_error():
    """主动上报当前异常（用于 try...except 中）"""
    _global_exception_handler(*sys.exc_info())