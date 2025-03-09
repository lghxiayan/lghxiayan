import logging.config

# import logging
import sys
import os

# 导入日志配置文件
logging.config.fileConfig('logging_ptvicomo.conf', encoding='utf-8')
logger = logging.getLogger('ptvicomo_log')
logger.setLevel(logging.INFO)

#
# # 配置日志记录器
# logger = logging.getLogger('ptvicomo_log')
# logger.setLevel(logging.INFO)
#
# # 创建控制台处理器
# console_handler = logging.StreamHandler(sys.stdout)  # 输出到标准输出
# console_handler.setLevel(logging.INFO)
#
# # 创建文件处理器
# file_handler = logging.FileHandler('selenium_ptvicomo_cookie_04.log', encoding='utf-8')  # 输出到文件
# file_handler.setLevel(logging.INFO)
#
# # 设置日志格式
# formatter = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s')
# console_handler.setFormatter(formatter)
# file_handler.setFormatter(formatter)
#
# # 添加处理器到日志记录器
# logger.addHandler(console_handler)
# logger.addHandler(file_handler)

if __name__ == '__main__':
    print(f"Python版本: {sys.version}")
    print(f"当前工作目录: {os.getcwd()}")

    logger.info(f"test!!!")
    logger.error(f"test error!!!")
    logger.info(f"test!!!")
