#
# Lightswitch - Enable / Disable Relay to switch outside lights on after sunset
#
# - Uses Astral module to determine 'astral dusk' time on current location
# - Enables Relay 1 (lights on) x minutes after 'astral dusk' time
# - Disables Relay 1 (lights off) at a certain time
#

import os
import sys
import argparse
from crontab import CronTab
from datetime import datetime, timedelta
try:
    import configparser
except:
    import ConfigParser as configparser
from pytz import timezone
from astral import Astral

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PYTHON_EXECUTABLE = sys.executable


def get_current_suntimes(location_city_name):
    a = Astral()
    a.solar_depression = 'civil'
    city = a[location_city_name]
    return city.sun(date=datetime.today(), local=True)


def parse_config(file):
    config = configparser.ConfigParser()
    try:
        config.read_file(file)
    except:
        config.readfp(file)
    return config


def parse_args():
    parser = argparse.ArgumentParser(description='Control Devantech Ethernet Relays - Cron updater')
    parser.add_argument('--config', default='config.ini',
                        help="Name of config file to use")
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()

    # Get config settings
    config = parse_config(open(os.path.join(CURRENT_DIR, args.config)))
    settings = dict(config.items('settings'))

    # Calculate begin and endtime
    suninfo = get_current_suntimes(settings['locationcity'])
    time_location_name = timezone('%s/%s' % (settings['locationregion'], settings['locationcity']))
    now = datetime.now(time_location_name)
    begintime = suninfo['dusk'] + timedelta(minutes=int(settings['sunduskoffsetminutes']))
    endtime = now.replace(hour=int(settings['endtimehour']), minute=int(settings['endtimeminute']))

    # Update crontab
    cron = CronTab(user=settings['cronuser'])
    commentstr = ' relay %s on %s:%s' % (settings['relay-id'], settings['erhost'], settings['erport'])
    for t in ['Enable', 'Disable']:
        cron.remove_all(comment='%s %s' % (t, commentstr))
    job_sr_on = cron.new(command='%s %s/relay_control.py %s on --host %s --port %s' %
                                 (PYTHON_EXECUTABLE, CURRENT_DIR, settings['relay-id'],
                                  settings['erhost'], settings['erport']),
                         comment='Enable %s' % commentstr)
    job_sr_off = cron.new(command='%s %s/relay_control.py %s off --host %s --port %s' %
                                  (PYTHON_EXECUTABLE, CURRENT_DIR, settings['relay-id'],
                                   settings['erhost'], settings['erport']),
                          comment='Disable %s' % commentstr)
    job_sr_on.setall(begintime.time())
    job_sr_off.setall(endtime.time())
    cron.write()
