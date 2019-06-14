# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------
from netease.database_pool import database_pool
import pymysql
import config
import logger

log = logger.loggler()


class database_tool:
    """
    数据库工具类

    """

    def __init__(self, database_host=config.database_host, database_port=config.database_port,
                 database_user_name=config.database_user_name, database_user_pwd=config.database_user_pwd,
                 database_name=config.database_name, database_charset=config.database_charset):
        """
        初始化数据库连接池

        :param database_host: 数据库位置
        :param database_port: 数据库端口
        :param database_user_name: 用户名
        :param database_user_pwd: 密码
        :param database_name: 数据库名
        :param database_charset: 数据库字符类型
        """
        self.conn = None
        try:
            self.pool = database_pool(database_host=database_host, database_port=database_port,
                                      database_user_name=database_user_name, database_user_pwd=database_user_pwd,
                                      database_name=database_name, database_charset=database_charset)
            log.debug("database create pool success", "")
        except Exception as e:
            log.error("database create pool failed", "")

    def __connect(self):
        """
        建立数据库连接

        """
        try:
            self.conn = self.pool.connect()
            log.debug("database connect success", "")
            return True
        except Exception as e:
            log.error("database connect failed", "")
            return False

    def execute(self, sql):
        """
        execute语句

        :param sql: sql语句
        :return:
        """
        if self.__connect():
            cursor = self.conn.cursor()
            try:
                cursor.execute(sql)
                log.debug("database execute success", "sql:{}".format(sql))
                return True
            except Exception as e:
                log.error("database execute failed", "sql:{},error:{}".format(sql, e))
                return False


if __name__ == "__main__":
    tool = database_tool()
    tool.execute("insert into user(user_id,user_name) values(474252223,'IsolationTom') ")
