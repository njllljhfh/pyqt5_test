# -*- coding:utf-8 -*-
import os
import re
import logging.config
import sys
from logging import Filter

# 项目名(根据你的项目名称修改)

PROJECT_NAME = 'pyqt5_test'
# 日志文件所在文件夹的名称（如：logs）
LOG_FOLDER_NAME = 'logs'

"""========================================="""
"""=         logging configuration         ="""
"""========================================="""

p = os.path.dirname(os.path.abspath(__file__))
# print(p)
sys.path.append(p)


class OperationType(object):
    run = {"op_type": "run"}
    walk = {"op_type": "walk"}
    fly = {"op_type": "fly"}


class MyFilter(Filter):

    def filter(self, record):
        """
        Determine if the specified record is to be logged.

        Is the specified record to be logged? Returns 0 for no, nonzero for
        yes. If deemed appropriate, the record may be modified in-place.
        """

        print("- - - - - - log filter begin- - - - - -")
        try:
            my_key = record.op_type
        except Exception:
            my_key = None
        if my_key:
            print("MyFilter -- OperationType = {}".format(my_key))
            import json
            print("msg = {}, ".format(record.msg))
            print("type(record.msg) = {}, ".format(record.msg))
            msg_dict = json.loads(record.msg)
            print("msg_dict = {}, ".format(msg_dict))
            print("type(msg_dict) = {}, ".format(msg_dict))

            xxx = json.loads(str({'a': 1}))
            print("xxx = {}, ".format(xxx))

        print("- - - - - - log filter end- - - - - -")

        return True  # 会输入log到控制台
        # return False # 只执行此filter中的逻辑，不会打印数据到控制台


class Log(object):
    log_directory = None  # log文件所在的目录

    @classmethod
    def isdir_logs(cls):
        """
        判断日志文件是否存在，不存在则创建
        :return:
        """
        if cls.log_directory is None:
            # 当前文件的目录(当settings.py文件)
            basedir = os.path.dirname(os.path.abspath(__file__))
            # print(f"basedir = {basedir}")
            pattern = r'(.*[/\\]%s)' % PROJECT_NAME
            # print(f"pattern = {pattern}")
            project_dir = re.search(pattern, basedir).group()
            # print(f"project_dir = {project_dir}")
            # logs文件的路径
            cls.log_directory = os.path.join(project_dir, LOG_FOLDER_NAME)

        # 判断日志文件夹是否在项目文件中
        # print(f"log_path = {cls.log_directory}")
        if not os.path.exists(cls.log_directory):
            os.mkdir(cls.log_directory)

    @classmethod
    def log_file_abspath(cls, log_file_name):
        cls.isdir_logs()
        abspath = cls.log_directory + '/' + log_file_name
        return abspath

    # @staticmethod
    # def make_logger(name=None):
    #     """
    #     1. 如果不传name，则根据__name__去loggers里查找__name__对应的logger配置(__name__为调用文件名)
    #     获取logger对象通过方法logging.getLogger(__name__)，不同的文件__name__不同，这保证了打印日志时标识信息不同，
    #     2. 如果传name,则根据name获取loggers对象
    #     3. 如果拿着name或者__name__去loggers里找key名时却发现找不到，于是默认使用key=''的配置
    #     :return: logger
    #     """
    #     logging.config.dictConfig(LOGGING_DIC)  # 导入上面定义的logging配置
    #     if name:
    #         logger = logging.getLogger(name)
    #     else:
    #         logger = logging.getLogger(__name__)
    #     return logger


# 定义日志输出格式
COMPLEXITY = '[%(levelname)s][%(asctime)s][%(threadName)s:%(thread)d][task_id:%(name)s]' \
             '\n[%(filename)s:%(lineno)d][%(message)s]'
STANDARD = "%(asctime)s  %(levelname)-6s module:%(name)s [line:%(lineno)d] %(message)s"
# 日志配置
LOGGING_DIC = {
    'version': 1,
    # 禁用已经存在的logger实例
    'disable_existing_loggers': False,
    # 日志格式化(负责配置log message 的最终顺序，结构，及内容)
    'formatters': {
        'complexity': {
            'format': COMPLEXITY
        },
        'standard': {
            'format': STANDARD
        }
    },
    # 过滤器，决定哪个log记录被输出
    'filters': {
        'console_filter': {  # 自定义的过滤类
            '()': 'settings.MyFilter',
        }
    },
    # 负责将Log message 分派到指定的destination
    'handlers': {
        # 打印到终端的日志
        'console': {
            'level': 'DEBUG',  # handler中的level等级大于等于logger的level时才生效。若小于，则按logger的level进行输出日志
            'class': 'logging.StreamHandler',  # 打印到屏幕
            'formatter': 'standard',
            'filters': ['console_filter'],  # 设置过滤器
        },
        # 打印到common文件的日志,收集info及以上的日志
        'file_error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件
            'formatter': 'standard',
            'filename': Log.log_file_abspath('error.log'),  # 日志文件路径
            'maxBytes': 1024 * 1024 * 5,  # 日志大小 5M
            'backupCount': 5,  # 备份5个日志文件
            'encoding': 'utf-8',  # 日志文件的编码，再也不用担心中文log乱码了
        },
        # 打印到importance文件的日志,收集error及以上的日志
        'file_debug': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件
            'formatter': 'standard',
            'filename': Log.log_file_abspath('debug.log'),  # 日志文件
            'maxBytes': 1024 * 1024 * 5,  # 日志大小 5M
            'backupCount': 5,  # 备份5个日志文件
            'encoding': 'utf-8',  # 日志文件的编码，再也不用担心中文log乱码了
        },
    },
    # logger实例
    'loggers': {
        # 默认的logger应用如下配置,
        # logging.getLogger(__name__)生成的不确定名字的logger都会使用默认logger,
        # 默认的logger会用'root'中的配置。
        '': {
            # 'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,  # 不向上（更高level的logger）传递
        },
        # 'default': {
        #     'handlers': ['console', 'common', 'importance'],
        #     'level': 'INFO',
        #     'propagate': True,  # 向上（更高level的logger）传递
        # },
        # 'common': {
        #     'handlers': ['console', 'common'],  # 这里把上面定义的两个handler都加上，即log数据既写入文件又打印到控制台
        #     'level': 'INFO',
        #     'propagate': True,  # 向上（更高level的logger）传递
        # },
        # 'importance': {
        #     'handlers': ['console', 'importance'],  # 这里把上面定义的两个handler都加上，即log数据既写入文件又打印到控制台
        #     'level': 'ERROR'
        # },

    },
    'root': {
        # 'handlers': ['console', 'file_error', 'file_debug'],  # 在控制台和指定的文件中写入日志
        # 'handlers': ['console'],  # 只输出日志到控制台
        'handlers': ['console', 'file_error'],  # 输出日志到控制台、错误日志
        'level': 'DEBUG',
        # 'level': 'ERROR',
    },
}

logging.config.dictConfig(LOGGING_DIC)  # 激活logging配置字典：LOGGING_DIC

"""==========================="""
"""=         其他配置         ="""
"""==========================="""
# if __name__ == '__main__':
#     logger = logging.getLogger(__name__)
#     logger.info("666", extra=OperationType.run)
