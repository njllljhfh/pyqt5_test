# -*- coding:utf-8 -*-
import logging
from random import choice


class ContextFilter(logging.Filter):
    ip = 'IP'
    username = 'USER'

    def filter(self, record):
        record.ip = self.ip
        record.username = self.username
        print("执行了么")
        return True


if __name__ == '__main__':
    levels = (logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL)
    users = ['Tom', 'Jerry', 'Peter']
    ips = ['113.108.98.34', '219.238.78.91', '43.123.99.68']

    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)-15s %(name)-5s %(levelname)-8s %(ip)-15s %(username)-8s %(message)s')
    logger = logging.getLogger('myLogger')
    filter = ContextFilter()
    logger.addFilter(filter)
    logger.debug('A debug message')
    logger.info('An info message with %s', 'some parameters')
