#
# Lightswitch - Enable / Disable Relay to switch outside lights on after sunset
#
# - Uses Astral module to determine 'astral dusk' time on current location
# - Enables Relay 1 (lights on) x minutes after 'astral dusk' time
# - Disables Relay 1 (lights off) at a certain time
#

import os
from crontab import CronTab
from datetime import datetime, timedelta
try:
    import configparser
except:
    import ConfigParser as configparser
from pytz import timezone
from astral import Astral


LOCATION_CITY_NAME = 'Amsterdam'
LOCATION_REGION = 'Europe'
SUN_DUSK_OFFSET_MINUTES = -10
CRON_USER = 'lennart'
CURRENT_DIR = os.path.join(os.path.expanduser("~"), 'devantech-ethernet-relay-control')


def get_current_suntimes(location_city_name):
    a = Astral()
    a.solar_depression = 'civil'
    city = a[location_city_name]
    return city.sun(date=datetime.today(), local=True)


def parse_config(file):
    config = configparser.ConfigParser()
    config.read_file(file)
    return config


if __name__ == '__main__':
    # Get config settings
    config = parse_config(open('config.ini'))
    settings = dict(config.items('settings'))

    # Calculate begin and endtime
    suninfo = get_current_suntimes(settings['locationcity'])
    time_location_name = timezone('%s/%s' % (settings['locationregion'], settings['locationcity']))
    now = datetime.now(time_location_name)
    begintime = suninfo['dusk'] + timedelta(minutes=int(settings['sunduskoffsetminutes']))
    endtime = now.replace(hour=int(settings['endtimehour']), minute=int(settings['endtimeminute']))

    # Update crontab
    cron = CronTab(user=settings['cronuser'])
    cron.remove_all(command='relay_control')
    job_sr_on = cron.new(command='/usr/bin/python %s/relay_control.py 1 on' % CURRENT_DIR)
    job_sr_off = cron.new(command='/usr/bin/python %s/relay_control.py 1 off' % CURRENT_DIR)
    job_sr_on.setall(begintime.time())
    job_sr_off.setall(endtime.time())
    cron.write()
