#
# Relay Control - Enable / Disable Relays from commandline
#
# Usage: relay_control.py <relay_id> <command:on/off> [<host>] [<port>]
#
# (c) 2017 April - Lennart Jongeneel
#

import socket
import argparse

ERCONTROL_HOST = 'ds1242'
ERCONTROL_PORT = 17123
BUFFER_SIZE = 255
ERCONTROL_COMMAND = 'SR'


def parse_args():
    parser = argparse.ArgumentParser(description='Control Devantech Ethernet Relays')
    parser.add_argument('relay_id', type=int, help='ID number of relay')
    parser.add_argument('command', type=str, help="Command: 'on' or 'off'")
    parser.add_argument('--host', default=ERCONTROL_HOST,
                        help="Hostname or IP-address of Ethernet Relay Control device")
    parser.add_argument('--port', type=int, default=ERCONTROL_PORT,
                        help="Control port of Ethernet Relay Control device")
    return parser.parse_args()


class MySocket:

    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def connect(self, host, port):
        self.sock.connect((host, port))

    def check_type(self):
        self.sock.send(b'\x10')
        res = s.sock.recv(BUFFER_SIZE)
        if res[0] != '\x12':
            print("Wrong module type found")
            return False
        else:
            return True


if __name__ == '__main__':
    # Parse argument and create command for Ethernet relay
    args = parse_args()
    command = ' '.join([ERCONTROL_COMMAND, str(args.relay_id), args.command])
    print("Send command '%s' to %s:%d" % (command, args.host, args.port))

    # Connect to device and send command
    s = MySocket()
    s.connect(args.host, args.port)
    if not s.check_type():
        s.sock.send(command.encode())
        data = s.sock.recv(BUFFER_SIZE)
        print("Response: %s" % data.strip().decode('utf8'))
