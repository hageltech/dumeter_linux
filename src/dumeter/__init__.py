
NAME = 'dumeter'
VERSION = '1.0b'
DB_VERSION = 1

DEFAULT_DATABASE_PATH = '/var/lib/' + NAME + '/db.sqlite'
DEFAULT_CONF_PATH = '/etc/' + NAME + '.conf'
REPORT_FREQUENCY = 120*60 # How often to report to dumeter.net, in seconds.
SLEEP_BETWEEN_UPDATES = 60 # How often to collect statistics, in seconds.
DEBUG = True

class DuMeterError(IOError):
    pass

