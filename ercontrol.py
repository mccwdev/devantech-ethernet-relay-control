#
# Module to control Devantech Ethernet Relay control
#

from datetime import datetime, timezone, timedelta
from astral import Astral
import socket


LOCATION_CITY_NAME = 'Amsterdam'
ERCONTROL_HOST = 'ds1242'
ERCONTROL_PORT = 17123
BUFFER_SIZE = 255
SUN_DUSK_OFFSET_MINUTES = 0
ERCONTROL_COMMAND_ON = 'SR 1 on'.encode('utf8')
ERCONTROL_COMMAND_OFF = 'SR 1 off'.encode('utf8')


def get_current_suntimes(location_city_name):
    a = Astral()
    a.solar_depression = 'civil'
    city = a[location_city_name]
    return city.sun(date=datetime.today(), local=True)


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
    suninfo = get_current_suntimes(LOCATION_CITY_NAME)
    now = datetime.now(timezone.utc)
    d = datetime.now(timezone.utc).astimezone()
    utc_offset = int((d.utcoffset() // timedelta(seconds=1)) / 3600)
    endtime = now.replace(hour=23-utc_offset, minute=30, second=0, microsecond=0)

    if suninfo['dusk'] < now and datetime.now(timezone.utc) < endtime:
        print("Enable Relay")
        s.sock.send(ERCONTROL_COMMAND_ON)
        data = s.sock.recv(BUFFER_SIZE)
        print(data)
    else:
        print("Disable Relay")
        s.sock.send(ERCONTROL_COMMAND_OFF)
        data = s.sock.recv(BUFFER_SIZE)
        print(data)
