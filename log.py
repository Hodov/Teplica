import logging
import settings

logger = logging.getLogger('main')


def init():
    log_level = settings.get_log_level()
    formatter = logging.Formatter(u'%(threadName)s %(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s] %(message)s')
    ch = logging.StreamHandler()
    fh = logging.FileHandler(u'logfile.log')
    if log_level == 'debug':
        level = logging.DEBUG
    elif log_level == 'info':
        level = logging.INFO
    elif log_level == 'warning':
        level = logging.WARNING
    elif log_level == 'error':
        level = logging.ERROR
    else:
        level = logging.CRITICAL
    logger.setLevel(level)
    fh.setLevel(level)
    ch.setLevel(logging.ERROR)
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    logger.addHandler(ch)
    logger.addHandler(fh)
