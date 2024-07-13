import logging
from colorlog import ColoredFormatter

# 用编程的方式来写一下高级的用法。
# 这种方式不推荐，因为要修改日志输出的级别的时候，需要修改源代码，这会造成程序的停止，在大型项目上是绝对不允许的。
# 更多的是使用logging.conf来配置

# 记录器
logger = logging.getLogger('baidu.com.applog')
logger.setLevel(logging.DEBUG)

# 屏幕处理器
consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.DEBUG)

# 文件处理器
fileHandler = logging.FileHandler('addDemo.log', encoding='utf-8', mode='w')
fileHandler.setLevel(logging.INFO)

# formatter格式
# 这里设置了两个格式化器，formatter用于文件输出，color_formatter用于屏幕输出
# 例如：%(levelname)-10s,格式统一为%()s，10表示占10个字符，-表示左对齐
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)-10s - %(message)s')
color_formatter = ColoredFormatter('%(log_color)s%(asctime)s - %(name)s - %(levelname)-10s - %(message)s',
                                   datefmt='%Y-%m-%d %H:%M:%S',
                                   log_colors={
                                       'DEBUG': 'cyan',
                                       'INFO': 'green',
                                       'WARNING': 'yellow',
                                       'ERROR': 'red',
                                       'CRITICAL': 'red,bg_white'
                                   },
                                   reset=True,
                                   style='%',
                                   secondary_log_colors={},
                                   )
# 给处理器设置格式
consoleHandler.setFormatter(color_formatter)
fileHandler.setFormatter(formatter)

# 将处理器添加到记录器中去
logger.addHandler(consoleHandler)
logger.addHandler(fileHandler)

# 定义一个或多个过滤器，可以对记录器和处理器起作用。
# 只有包括baidu.com的日志才会输出
flt = logging.Filter('baidu.com')

# 处理器关联过滤器
fileHandler.addFilter(flt)
# logger.addFilter(flt)

# 输出
logger.debug('Something bad could happen!debug')
logger.info('Something bad could happen!info')
logger.warning('Something bad could happen!warning')
logger.error('Aw snap! Everything failed.error')
logger.critical('You are running the program.critical')
