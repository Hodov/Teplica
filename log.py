import logging
import settings


def init():
    log_level = settings.get_log_level()
    if log_level == 'debug':
        logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s] %(message)s',
                            level=logging.DEBUG,
                            filename=u'logfile.log')
    elif log_level == 'info':
        logging.basicConfig(level=logging.INFO,
                            filename=u'logfile.log')
    elif log_level == 'warning':
        logging.basicConfig(level=logging.WARNING,
                            filename=u'logfile.log')
    elif log_level == 'error':
        logging.basicConfig(level=logging.ERROR)
    else:
        logging.basicConfig(level=logging.CRITICAL)
