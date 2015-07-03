import os
import socket
import threading
import pickle
import modules.package as package
import modules.log as log


class Server:
    def __init__(self):
        self.HOST = ''
        self.PORT = ''
        self.CLIENTS = []

        self.loadconfigfile(self)
        self.run()

    @staticmethod
    def loadconfigfile(self):
        if os.path.exists('settings.txt'):
            file = open('settings.txt', 'r')
            for i in file:
                if not i.startswith('#'):
                    data = i.split('=')
                    if data[0] == 'HOST':
                        self.HOST = data[1]
                    elif data[0] == 'PORT':
                        self.PORT = int(data[1].strip())
            log.writelog('Конфигурационный файл загружен')
        else:
            log.writelog('Конфигурационный файл не найден')

    def handler(self, clientsocket, cliendaddr):
        log.writelog('Клиент %s подключился' % cliendaddr[0])
        self.CLIENTS.append(clientsocket)

        while 1:
            data = clientsocket.recv(1024)
            if not data:
                clientsocket.close()
                break
            else:
                result = pickle.loads(data)
                awnser = package.parse(result)
                if len(awnser) > 0:
                    clientsocket.send(pickle.dumps(awnser))
                    awnser.clear()

        clientsocket.close()

    def run(self):
        sock = socket.socket()
        sock.bind(('', self.PORT))
        sock.listen(2)
        log.writelog('Сервер запущен на %s' % self.HOST)

        while 1:
            conn, addr = sock.accept()
            thread = threading.Thread(target=self.handler, args=(conn, addr)).start()
        sock.close()
