# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------
import logging
import config


def singleton(cls):
    instances = {}

    def _singleton(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return _singleton


@singleton
class loggler_tool:
    """
    日志工具类（单例模式）

    """

    def __init__(self, logger_file=config.logger_file, logger_name=config.logger_name,
                 logger_path=config.logger_path,
                 logger_formatter=config.logger_formatter, logger_console_level=config.logger_console_level,
                 logger_file_level=config.logger_file_level):
        """
        初始化logger

        :param logger_name: 日志名
        :param logger_path: 日志文件路径
        :param logger_formatter: 日志输出格式
        :param loggler_console_level: 日志终端输出等级
        :param logger_file_level: 日志文件输出等级
        """
        self.logger_file = logger_file

        # 创建logger
        self.logger = logging.getLogger(name=logger_name)
        self.logger.setLevel(level=logger_console_level)

        # 创建console handler
        self.console_handler = logging.StreamHandler()
        self.console_handler.setLevel(level=logger_file_level)

        # 创建file handler
        self.file_handler = logging.FileHandler(filename=logger_path)
        self.file_handler.setLevel(level=logger_file_level)

        # 创建formatter
        self.formatter = logging.Formatter(fmt=logger_formatter)

        self.console_handler.setFormatter(self.formatter)
        self.file_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.console_handler)
        self.logger.addHandler(self.file_handler)

    def debug(self, logger_file=config.logger_file, message=""):
        self.logger.debug("{} => {}".format(logger_file, message))

    def info(self, logger_file=config.logger_file, message=""):
        self.logger.info("{} => {}".format(logger_file, message))

    def warning(self, logger_file=config.logger_file, message=""):
        self.logger.warning("{} => {}".format(logger_file, message))

    def error(self, logger_file=config.logger_file, message=""):
        self.logger.error("{} => {}".format(logger_file, message))

    def critical(self, logger_file=config.logger_file, message=""):
        self.logger.critical("{} => {}".format(logger_file, message))


if __name__ == '__main__':
    log = loggler_tool()
    log.debug("test1", 'This is a customer debug message')
    log.info("test2", 'This is an customer info message')
    log.warning('This is a customer warning message')
    log.error('This is an customer error message')
    log.critical('This is a customer critical message')
