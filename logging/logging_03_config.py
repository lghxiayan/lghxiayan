import logging.config

# 使用colorlog库的时候，并不需要在源码中导入colorlog
# 用配置文件的方式来写一下高级的用法。使用logging.conf来配置

# 记录器

logging.config.fileConfig('logging.conf', encoding='utf-8')
logger = logging.getLogger('applog')

# 输出
logger.debug('Something bad could happen!debug')
logger.info('Something bad could happen!info')
logger.warning('Something bad could happen!warning')
logger.error('Aw snap! Everything failed.error')
logger.critical('You are running the program.critical')

a = 'abc'
try:
    int(a)
except Exception as e:
    logger.exception(e)
