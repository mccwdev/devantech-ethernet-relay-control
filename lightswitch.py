#
# Lightswitch - Enable Relay to switch outside lights on after sunset
#
# - Uses Astral module to determine 'astral dusk' time on current location
# - Enables Relay 1 (lights on) x minutes after 'astral dusk' time
# - Disables Relay 1 (lights off) at a certain time
#

from datetime import datetime, timedelta
from pytz import timezone
import socket
from astral import Astral


LOCATION_CITY_NAME = 'Amsterdam'
LOCATION_REGION = 'Europe'
ERCONTROL_HOST = 'ds1242'
ERCONTROL_PORT = 17123
BUFFER_SIZE = 255
SUN_DUSK_OFFSET_MINUTES = -10
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
    time_location_name = timezone('%s/%s' % (LOCATION_REGION, LOCATION_CITY_NAME))
    now = datetime.now(time_location_name)
    endtime = now.replace(hour=23, minute=30)

    if (suninfo['dusk'] + timedelta(minutes=SUN_DUSK_OFFSET_MINUTES)) < now < endtime:
        print("Enable Relay")
        s.sock.send(ERCONTROL_COMMAND_ON)
        data = s.sock.recv(BUFFER_SIZE)
        print(data)
    else:
        print("Disable Relay")
        s.sock.send(ERCONTROL_COMMAND_OFF)
        data = s.sock.recv(BUFFER_SIZE)
        print(data)
