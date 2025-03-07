"""
wowjump_数据配置文件
"""

# 配置项
CONFIG = {
    # 指定进程名为"wow.exe",在win11中不区分大小写，但在编程的过程中，统一使用小写
    "PROCESS_NAME": "wow.exe",
    # never_end_wow 中文版魔兽世界，指定窗口标题为"魔兽世界"
    "WINDOW_TITLE": "魔兽世界",
    # 不管是直接运行，还是使用加速器运行，都能找到该类名
    "WOW_CLASS_NAME": "GxWindowClassD3d",

    # 需要按下的键列表，包括 'W', 'B', '2'
    "KEYS_TO_PRESS": ['W'],
    # 每个按键之间的间隔时间为1秒。
    "INTERVAL_BETWEEN_KEYS": 1,
    # 重试次数为3次。
    "RETRY_ATTEMPTS": 3,

    # 随机睡眠时间范围为1到5秒
    "SLEEP_TIME_RANGE": (1, 50)
}
