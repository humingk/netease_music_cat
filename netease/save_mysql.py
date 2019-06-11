# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------
import pymysql
import config
import logger
log=logger.loggler()


class save_mysql:
    """
    mysql数据库操作类

    """

    def __init__(self, database_user_name=config.database_user_name, database_user_pwd=config.database_user_pwd,
                 database_name=config.database_name, database_charset=config.database_charset):
        """
        操作类初始化

        :param database_user_name: 用户名
        :param database_user_pwd: 密码
        :param database_name: 数据库名
        :param database_charset: 数据库字符类型
        """

        self.__database_user_name = database_user_name
        self.__database_user_pwd = database_user_pwd
        self.__database_name = database_name
        self.__database_charset = database_charset

        self.__conn = self.__connect()

    def __connect(self):
        """
        数据库连接

        """
        try:
            self.__conn = pymysql.connect("localhost", self.__database_user_name, self.__database_user_pwd,
                                          self.__database_name, self.__database_charset)
            log.debug("save_mysql","connect mysql success")
        except Exception as e:
            self.__conn=False
            log.error("save_mysql","connect mysql failed:{}".format(e))

    def __insert(self,sql):
        if self.__conn:
            cursor=self.__conn.cursor()
        else:
            return False



    def insert_playlists(self,result):
        if result[0]:
            for playlist in result[1]:
                self.__insert("INSERT IGNORE INTO ")


    # def save_comments(self):
    #
    #     # 游标对象
    #     if (self)
    #         cursor = self.__conn.cursor()
    #
    #     # comment_data数据
    #     table_comment_name = config.table_comment_name
    #     table_comment_cols = config.table_comment_cols
    #
    #     for i in range(len(self.comment_data)):
    #
    #         # 存放comment_data[i]中的value
    #         comment_values = []
    #         if self.comment_data is not None:
    #             for k, v in self.comment_data[i].items():
    #                 comment_values.append(v)
    #
    #             comment_insert_sql = "INSERT IGNORE INTO %s (%s) VALUES (%s)" % (
    #                 str(table_comment_name), str(table_comment_cols), str(comment_values).strip("[]"))
    #
    #             # 移除已经添加到数据库的comment_data字典元素
    #             delete_dict_comment = {}
    #             if self.comment_data is not None:
    #                 delete_dict_comment = self.comment_data[i]
    #                 # error :待修改
    #                 # del self.comment_data[i]
    #
    #             try:
    #                 cursor.execute(comment_insert_sql)
    #                 db.commit()
    #                 if len(comment_insert_sql) % 1000 == 0:
    #                     print(str(len(comment_insert_sql)) + "-->")
    #             except pymysql.err as e:
    #                 print("插入数据表失败！...")
    #                 print(e)
    #                 db.rollback()
    #
    #     # user_data数据
    #     table_user_name = config.table_user_name
    #     table_user_cols = config.table_user_cols
    #
    #     for i in range(len(self.user_data)):
    #
    #         # 存放user_data[i]中的value
    #         user_values = []
    #         if self.user_data is not None:
    #             for k, v in self.user_data[i].items():
    #                 user_values.append(v)
    #
    #             user_insert_sql = "INSERT IGNORE INTO %s (%s) VALUES (%s)" % (
    #                 str(table_user_name), str(table_user_cols), str(user_values).strip("[]"))
    #
    #             # 移除已经添加到数据库的user_data字典元素
    #             delete_dict_user = {}
    #             if self.user_data is not None:
    #                 delete_dict_user = self.user_data[i]
    #                 # del self.user_data[i]
    #
    #             try:
    #                 cursor.execute(user_insert_sql)
    #                 db.commit()
    #             except pymysql.err as e:
    #                 print("插入数据表失败！...")
    #                 print(e)
    #                 db.rollback()
    #
    #     # 关闭数据库
    #     db.close()


if __name__ == "__main__":
    save=save_mysql()
