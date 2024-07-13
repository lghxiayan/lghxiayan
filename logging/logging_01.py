import logging

FORMAT = '%(asctime)s, %(clientip)-15s %(user)-8s %(message)s'
logging.basicConfig(level=logging.DEBUG, format=FORMAT)  # We'll talk about this sonn!
d = {'clientip': '192.168.0.1', 'user': 'fbloggs'}
logger = logging.getLogger('tcpserver')
logger.setLevel(logging.INFO)

sh = logging.StreamHandler()
fh = logging.FileHandler('tcpserver.log', mode='w', encoding='utf-8', delay=False)
logger.addHandler(sh)

logger.warning('Protocol problem: %s', 'connection reset', extra=d)
# logger.warning( extra=d)
# logging.warning('Something bad could happen!')
# logging.info('You are running the program')
# logging.error('Aw snap! Everything failed.')
