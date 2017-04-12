#
# Lightswitch - Enable / Disable Relay to switch outside lights on after sunset
#
# - Uses Astral module to determine 'astral dusk' time on current location
# - Enables Relay 1 (lights on) x minutes after 'astral dusk' time
# - Disables Relay 1 (lights off) at a certain time
#

from crontab import CronTab
from datetime import datetime, timedelta
from pytz import timezone
from astral import Astral


LOCATION_CITY_NAME = 'Amsterdam'
LOCATION_REGION = 'Europe'
SUN_DUSK_OFFSET_MINUTES = -10
CRON_USER = 'lennart'
CURRENT_DIR = '/home/lennart/code/devantech-ethernet-relay-control/'


def get_current_suntimes(location_city_name):
    a = Astral()
    a.solar_depression = 'civil'
    city = a[location_city_name]
    return city.sun(date=datetime.today(), local=True)


if __name__ == '__main__':
    # Calculate begin and endtime
    suninfo = get_current_suntimes(LOCATION_CITY_NAME)
    time_location_name = timezone('%s/%s' % (LOCATION_REGION, LOCATION_CITY_NAME))
    now = datetime.now(time_location_name)
    begintime = suninfo['dusk'] + timedelta(minutes=SUN_DUSK_OFFSET_MINUTES)
    endtime = now.replace(hour=23, minute=30)

    # Update crontab
    cron = CronTab(user=CRON_USER)
    cron.remove_all(command='relay_control')
    job_sr_on = cron.new(command='/usr/bin/python %s/relay_control.py 1 on' % CURRENT_DIR)
    job_sr_off = cron.new(command='/usr/bin/python %s/relay_control.py 1 off' % CURRENT_DIR)
    job_sr_on.setall(begintime.time())
    job_sr_off.setall(endtime.time())
    cron.write()
