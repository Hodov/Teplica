import logging
import settings

logger = logging.getLogger('main')


def init():
    print 'Log level'
    log_level = settings.get_log_level()
    print log_level
    print 'Formatter'
    formatter = logging.Formatter(u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s] %(message)s')
    print 'ch'
    ch = logging.StreamHandler()
    print 'fh'
    fh = logging.FileHandler(u'logfile.log')
    print 'If'
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
    print level
    print 'logger'
    logger.setLevel(level)
    fh.setLevel(level)
    ch.setLevel(logging.ERROR)
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    logger.addHandler(ch)
    logger.addHandler(fh)