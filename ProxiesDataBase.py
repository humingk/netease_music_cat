# table IPPORT
# ip_port TEXT NOT NULL
import sqlite3
import traceback
import config


def InitDB():
    db_conn = sqlite3.connect(config.DBName)
    try:
        db_conn.execute(
            """CREATE TABLE IF NOT EXISTS {} (IP_PORT TEXT NOT NULL);""".format(config.TabelName))
        db_conn.commit()
        return True
    except BaseException as e:
        db_conn.rollback()
        return False
    finally:
        db_conn.close()


def AddItem(ip_port):
    db_conn = sqlite3.connect(config.DBName)
    db_cursor = db_conn.cursor()

    try:
        db_conn.execute("""INSERT INTO {} VALUES ('{}');""".format(config.TabelName, ip_port))
        db_conn.commit()
    except BaseException as e:
        db_conn.rollback()
        traceback.print_exc()
    db_conn.close()


def AddItems(ip_list):
    if len(ip_list) < 1:
        return

    sql_str = """INSERT INTO IPPORT VALUES """

    for item in ip_list:
        sql_str += ("('{}'),".format(item))
    index = len(sql_str)
    sql_str = sql_str[0:index - 1]
    sql_str += ";"
    db_conn = sqlite3.connect(config.DBName)
    try:
        db_conn.execute(sql_str)
        db_conn.commit()
    except BaseException as e:
        db_conn.rollback()
        traceback.print_exc()
    db_conn.close()


def DelItem(item):
    db_conn = sqlite3.connect(config.DBName)

    try:
        db_conn.execute("""DELETE FROM {} WHERE IP_PORT = '{}';""".format(config.TabelName, item))
        db_conn.commit()
    except BaseException as e:
        db_conn.rollback()
        traceback.print_exc()
    finally:
        db_conn.close()


def ClearItems():
    db_conn = sqlite3.connect(config.DBName)
    try:
        db_conn.execute("""DELETE FROM {};""".format(config.TabelName))
        db_conn.commit()
    except BaseException as e:
        db_conn.rollback()
        traceback.print_exc()
    finally:
        db_conn.close()


def GetItems():
    ip_list = []
    db_conn = sqlite3.connect(config.DBName)
    db_cur = db_conn.cursor()
    try:
        for item in db_cur.execute("""SELECT * FROM {};""".format(config.TabelName)).fetchall():
            ip_list.append(item[0])
    except BaseException as e:
        traceback.print_exc()
    finally:
        db_conn.close()
        return ip_list
