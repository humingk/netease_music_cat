# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    数据库存储模块
        使用方式：
            save()

"""
class save:

    def __init__(self):

        database_user_name = config.database_user_name
        database_user_pwd = config.database_user_pwd
        database_name = config.database_name
        database_charset = config.database_charset

    # 将评论表、用户表存入数据库
    def save(self,type,content):

        # 连接数据库
        database_user_name = config.database_user_name
        database_user_pwd = config.database_user_pwd
        database_name = config.database_name
        database_charset = config.database_charset
        try:
            db = pymysql.connect("localhost", database_user_name, database_user_pwd, database_name,
                                 charset=database_charset)
        except pymysql.err as e:
            print("数据库连接失败！...")
            print(e)
        # 游标对象
        cursor = db.cursor()

        # comment_data数据
        table_comment_name = config.table_comment_name
        table_comment_cols = config.table_comment_cols

        for i in range(len(self.comment_data)):

            # 存放comment_data[i]中的value
            comment_values = []
            if self.comment_data is not None:
                for k, v in self.comment_data[i].items():
                    comment_values.append(v)

                comment_insert_sql = "INSERT IGNORE INTO %s (%s) VALUES (%s)" % (
                    str(table_comment_name), str(table_comment_cols), str(comment_values).strip("[]"))

                # 移除已经添加到数据库的comment_data字典元素
                delete_dict_comment = {}
                if self.comment_data is not None:
                    delete_dict_comment = self.comment_data[i]
                    # error :待修改
                    # del self.comment_data[i]

                try:
                    cursor.execute(comment_insert_sql)
                    db.commit()
                    if len(comment_insert_sql) % 1000 == 0:
                        print(str(len(comment_insert_sql)) + "-->")
                except pymysql.err as e:
                    print("插入数据表失败！...")
                    print(e)
                    db.rollback()

        # user_data数据
        table_user_name = config.table_user_name
        table_user_cols = config.table_user_cols

        for i in range(len(self.user_data)):

            # 存放user_data[i]中的value
            user_values = []
            if self.user_data is not None:
                for k, v in self.user_data[i].items():
                    user_values.append(v)

                user_insert_sql = "INSERT IGNORE INTO %s (%s) VALUES (%s)" % (
                    str(table_user_name), str(table_user_cols), str(user_values).strip("[]"))

                # 移除已经添加到数据库的user_data字典元素
                delete_dict_user = {}
                if self.user_data is not None:
                    delete_dict_user = self.user_data[i]
                    # del self.user_data[i]

                try:
                    cursor.execute(user_insert_sql)
                    db.commit()
                except pymysql.err as e:
                    print("插入数据表失败！...")
                    print(e)
                    db.rollback()

        # 关闭数据库
        db.close()

if __name__ == "__main__":
    save()