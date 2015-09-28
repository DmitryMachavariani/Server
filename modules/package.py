import pickle
import hashlib
import pymysql

import modules.log as log

conn = pymysql.connect(host='127.0.0.1', user='root', passwd='1752dima', db='my_skype')
cur = conn.cursor()
log.writelog('База данных подключена')


def buildpackage(type, data):
    content = [i for i in data]
    presend = [type, content]

    presend = pickle.dumps(presend)
    return presend


def parse(package):
    result = []
    if package[0] == "login":
        username = package[1][0]
        password = hashlib.md5(package[1][1].encode('UTF-8')).hexdigest()
        cur.execute("SELECT * FROM tb_users WHERE username=%s AND password=%s", (username, password))
        if cur.fetchone() is None:
            result.append("login")
            result.append("failed")
        else:
            log.writelog("Успешная авторизация: " + package[1][0])
            result.append("login")
            result.append("success")

    if package[0] == "getfriend":
        username = package[1][0]
        cur.execute("SELECT friend_username FROM tb_friends WHERE username=%s", username)
        res = cur.fetchall()

        if res is None:
            result.append("None")
        else:
            result.append(res)

    return result
