# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------
import threading
from DBUtils.PooledDB import PooledDB
import pymysql
import config
from logger_tool import loggler_tool

logger = loggler_tool()


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
            mincached=5,
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
        self.conn = self.__connect()

    def __new__(cls, *args, **kwargs):
        if not hasattr(database_pool, "_instance"):
            with database_pool._instance_lock:
                if not hasattr(database_pool, "_instance"):
                    try:
                        database_pool._instance = object.__new__(cls, *args, **kwargs)
                        logger.debug("database create pool success", "")
                    except Exception as e:
                        logger.error("database create pool failed", "error:{}".format(e))
        return database_pool._instance

    def __connect(self):
        """
        建立数据库连接

        """
        try:
            self.conn = self.pool.connection()
            logger.debug("database connect success", "")
        except Exception as e:
            self.conn = None
            logger.error("database connect failed", "error:{}".format(e))
        return self.conn

    def execute(self, sql):
        """
        execute语句

        :param sql: sql语句
        :return:
        """
        try:
            self.conn.cursor().execute(sql)
            # logger.debug("database execute success", "sql:{}".format(sql))
            return True
        except pymysql.err.IntegrityError as e:
            logger.warning("database execute duplicate", "sql:{},error:{}".format(sql, e))
            return True
        except pymysql.err.DataError as e:
            logger.warning("database execute too long", "sql:{},error:{}".format(sql, e))
            return False
        except Exception as e:
            logger.error("database execute failed", "sql:{},error:{}".format(sql, e))
            return False

    def commit(self):
        try:
            self.conn.commit()
            # logger.debug("database commit success", "")
            return True
        except Exception as e:
            logger.error("database commit failed", "error:{}".format(e))
            return False


if __name__ == '__main__':
    for i in range(20):
        pool = database_pool()
        pool.execute("insert into user(user_id,user_name) values(474252223,'IsolationTom') ")
        pool.commit()
        print(id(pool))
