import datetime

def writelog(text):
    try:
        logfile = open('log.txt', 'a')
        data = '[%s] %s' % (datetime.datetime.today().now(), text)
        logfile.write(data + '\n')
        print(data)
    except Exception:
        logfile.write('В модуле ', __name__, ' возникла ошибка')
