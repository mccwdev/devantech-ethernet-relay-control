#
# Relay Test - Determine relay device type
#
# (c) 2017 April - Lennart Jongeneel
#

import socket

# ERCONTROL_HOST = 'ds1242'
# ERCONTROL_PORT = 17123
ERCONTROL_HOST = '192.168.7.80'
ERCONTROL_PORT = 17494
BUFFER_SIZE = 255


class MySocket:

    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def connect(self, host, port):
        self.sock.connect((host, port))

if __name__ == '__main__':
    s = MySocket()
    s.connect(ERCONTROL_HOST, ERCONTROL_PORT)

    s.sock.send(b'\x10')
    data = s.sock.recv(BUFFER_SIZE)
    print(data)
