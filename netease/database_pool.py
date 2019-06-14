# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------
import threading
from DBUtils.PooledDB import PooledDB
import pymysql
import config
import logger

log = logger.loggler()


class database_pool:
    """
    数据库连接池

    """
    _instance_lock = threading.Lock()

    def __init__(self, database_host=config.database_host, database_port=config.database_port,
                 database_user_name=config.database_user_name, database_user_pwd=config.database_user_pwd,
                 database_name=config.database_name, database_charset=config.database_charset):
        self.pool = PooledDB(
            # 使用数据库模块
            creator=pymysql,
            # 数据库最大连接数
            maxconnections=10,
            # 初始化时，链接池中至少创建的空闲的链接
            mincached=3,
            # 初始化时，链接池中至多创建的空闲的链接
            maxcached=10,
            # 链接池中最多共享的链接数量
            # PS: 无用，因为pymysql和MySQLdb等模块的 threadsafety都为1
            # 所有值无论设置为多少，_maxcached永远为0，所以永远是所有链接都共享
            maxshared=3,
            # 连接池中如果没有可用连接后，是否阻塞等待
            blocking=True,
            # 一个链接最多被重复使用的次数，None表示无限制
            maxusage=None,
            # 开始会话前执行的命令列表,如["set datestyle to ...", "set time zone ..."]
            setsession=[],
            # ping MySQL服务端，检查是否服务可用
            # 如：0 = None = never, 1 = default = whenever it is requested,
            # 2 = when a cursor is created, 4 = when a query is executed, 7 = always
            ping=0,
            host=database_host,
            port=database_port,
            user=database_user_name,
            password=database_user_pwd,
            database=database_name,
            charset=database_charset
        )

    def __new__(cls, *args, **kwargs):
        if not hasattr(database_pool, "_instance"):
            with database_pool._instance_lock:
                if not hasattr(database_pool, "_instance"):
                    database_pool._instance = object.__new__(cls, *args, **kwargs)
        return database_pool._instance

    def connect(self):
        return self.pool.connection()


if __name__ == '__main__':
    pool = database_pool()
    conn = pool.connect()
    cursor = conn.cursor()
    cursor.execute("insert into user(user_id,user_name) values(474252223,'IsolationTom') ")
