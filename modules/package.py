import pickle
import os

import modules.log as log


def buildpackage(type, data):
    content = [i for i in data]
    presend = [type, content]

    presend = pickle.dumps(presend)
    return presend


def parse(package):
    if package[0] == "login":
        if not os.path.isdir("users"):
            os.mkdir("users", 0o777)
        if os.path.isfile(os.path.join(os.path.curdir + "/users/", package[1][0])):
            file = open(os.path.join(os.path.curdir + "/users/" + package[1][0]))
            password = file.readline()
            file.close()

            if password.strip() == package[1][1]:
                log.writelog("Успешная авторизация: " + package[1][0])
