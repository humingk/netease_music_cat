# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------
import threading
from DBUtils.PooledDB import PooledDB
import pymysql
import config
from my_tools.logger_tool import loggler_tool

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
            maxconnections=100,
            # 初始化时，链接池中至少创建的空闲的链接
            mincached=20,
            # 初始化时，链接池中至多创建的空闲的链接
            maxcached=20,
            # 链接池中最多共享的链接数量
            # PS: 无用，因为pymysql和MySQLdb等模块的 threadsafety都为1
            # 所有值无论设置为多少，_maxcached永远为0，所以永远是所有链接都共享
            maxshared=100,
            # 连接池中如果没有可用连接后，是否阻塞等待
            blocking=True,
            # 一个链接最多被重复使用的次数，None表示无限制
            maxusage=None,
            # 开始会话前执行的命令列表,如["set datestyle to ...", "set time zone ..."]
            setsession=[],
            # ping MySQL服务端，检查是否服务可用
            # 如：0 = None = never, 1 = default = whenever it is requested,
            # 2 = when a cursor is created, 4 = when a query is executed, 7 = always
            ping=1,
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
        :return: 执行状态
        """
        try:
            self.conn.cursor().execute(sql)
            # logger.debug("database execute success", "sql:{}".format(sql))
            return True
        except pymysql.err.IntegrityError as e:
            # 键重复
            if e.args[0] == 1062:
                logger.debug("database execute duplicate", "sql:{},error:{}".format(sql, e))
                return False
            else:
                logger.error("database execute failed", "sql:{},error:{}".format(sql, e))
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

    # 表插入-----------------

    def insert_user(self, user_id, user_name=""):
        self.execute(
            "insert into user(user_id,user_name) values({},'{}')"
                .format(user_id, user_name)
        )

    def insert_ranklist(self, ranklist_id, ranklist_type=0, ranklist_date=""):
        self.execute(
            "insert into ranklist(ranklist_id, ranklist_type,ranklist_date) values('{}',{},{})"
                .format(ranklist_id, ranklist_type, ranklist_date)
        )

    def insert_song(self, song_id, song_name=""):
        self.execute(
            "insert into song(song_id,song_name) values ({},'{}')"
                .format(song_id, pymysql.escape_string(song_name))
        )

    def update_song_hot_comment_count(self, song_id, song_hot_comment_count=0):
        self.execute(
            "update song set song_hot_comment_count={} where song_id={}"
                .format(song_hot_comment_count, song_id)
        )

    def update_song_default_comment_count(self, song_id, song_default_comment_count=0):
        self.execute(
            "update song set song_default_comment_count={} where song_id={}"
                .format(song_default_comment_count, song_id)
        )

    def insert_user_ranklist(self, user_id, ranklist_id):
        self.execute(
            "insert into user_ranklist(user_id,ranklist_id) values ({},'{}')"
                .format(user_id, ranklist_id)
        )

    def insert_song_ranklist(self, song_id, ranklist_id, song_score):
        self.execute(
            "insert into song_ranklist(song_id,ranklist_id,song_score) values ({},'{}',{})"
                .format(song_id, ranklist_id, song_score)
        )

    def insert_playlist(self, playlist_id, playlist_name="", playlist_songs_total=0, playlist_play_count=0,
                        playlist_update_date=""):
        self.execute(
            "insert into playlist(playlist_id,playlist_name,playlist_songs_total,playlist_play_count,playlist_update_date) values ({},'{}',{},{},'{}')"
                .format(playlist_id, playlist_name, playlist_songs_total, playlist_play_count, playlist_update_date)
        )

    def insert_user_playlist(self, user_id, playlist_id, playlist_type):
        self.execute(
            "insert into user_playlist(user_id,playlist_id,playlist_type) values ({},{},{})"
                .format(user_id, playlist_id, playlist_type)
        )

    def insert_song_playlist(self, song_id, playlist_id, playlist_type):
        self.execute(
            "insert into song_playlist(song_id,playlist_id,playlist_type) values ({},{},{})"
                .format(song_id, playlist_id, playlist_type)
        )

    def insert_comment(self, comment_id, comment_type, comment_date, comment_content, comment_like_count):
        self.execute(
            "insert into comment(comment_id, comment_type, comment_date, comment_content,comment_like_count) values ({},{},'{}','{}',{})"
                .format(comment_id, comment_type, comment_date, pymysql.escape_string(comment_content),
                        comment_like_count)
        )

    def insert_song_comment(self, song_id, comment_id):
        self.execute(
            "insert into song_comment(song_id,comment_id) values ({},{})"
                .format(song_id, comment_id)
        )

    def insert_user_comment(self, user_id, comment_id):
        self.execute(
            "insert into user_comment(user_id,comment_id) values ({},{})"
                .format(user_id, comment_id)
        )

    def insert_artist(self, artist_id, artist_name="", artist_score=0):
        self.execute(
            "insert into artist(artist_id,artist_name,artist_score) values ({},'{}',{})"
                .format(artist_id, artist_name, artist_score)
        )

    def insert_artist_song(self, artist_id, song_id):
        self.execute(
            "insert into artist_song(artist_id,song_id) values ({},{})"
                .format(artist_id, song_id)
        )


if __name__ == '__main__':
    # for i in range(20):
    pool = database_pool()
    pool.execute("insert into user(user_id,user_name) values(474252223,'IsolationTom') ")
    # pool.execute("insert into user_comment(user_id, comment_id) values (111,222)")
    pool.commit()
    print(id(pool))
