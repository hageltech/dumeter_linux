#!/usr/bin/env python

VERSION = '1.0b'
DB_VERSION = 1
DEFAULT_DATABASE_PATH = '/var/lib/dumeter/db.sqlite'
DEFAULT_CONF_PATH = './reporter.conf'
DEBUG = True

import sys
import urllib
import urllib2
import ConfigParser
import sqlite3
import datetime
import logging
import logging.handlers

def setupLogging():
    global logger
    # TODO: Change process name: http://stackoverflow.com/questions/564695/is-there-a-way-to-change-effective-process-name-in-python
    logger = logging.getLogger(sys.argv[0])
    logger.setLevel(logging.DEBUG)
    if DEBUG:
        # Set up console logger if debugging
        cons = logging.StreamHandler()
        cons.setLevel(DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        cons.setFormatter(formatter)
        logger.addHandler(cons)
    # Set up normal syslog logger
    syslog = logging.handlers.SysLogHandler(facility=logging.handlers.SysLogHandler.LOG_DAEMON)
    logger.addHandler(syslog)

class DuMeterError(IOError):
    pass

# *****************************************************************************************************************
# *****************************************************************************************************************
# *****************************************************************************************************************
class Config:
    """ Parses/reads configuration file, ensures sensible defaults """

    def __init__(self):
        self.config = ConfigParser.ConfigParser({
            # Defaults go here!
        })
        self.config.read(DEFAULT_CONF_PATH)

    def reporters(self):
        """ List of all reporters in the config file """
        result = self.config.sections()
        if 'global' in result: result.remove('global')
        return result

    def dumeter_net_key(self, reporter):
        """ Key for a particular reporter """
        try:
            return self.config.get(reporter, 'link_code')
        except ConfigParser.Error:
            return None

    def interface(self, reporter):
        """ Interface to monitor for a particular reporter """
        try:
            return self.config.get(reporter, 'interface')
        except ConfigParser.Error:
            return None

    def database_file(self):
        """ Path to a database file """
        try:
            return self.config.get('global', 'database_file')
        except ConfigParser.Error:
            return DEFAULT_DATABASE_PATH



# *****************************************************************************************************************
# *****************************************************************************************************************
# *****************************************************************************************************************
class DuMeterNetReporter:
    """ This class communicates with dumeter.net service """

    PREFIX = 'http://dumeter.net/token/data.csv?'

    # *****************************************************************************************************************
    def url(self, token):
        """ Encode all needed parameters for dumeter.net URL """
        return self.PREFIX + urllib.urlencode({'token': token})

    # *****************************************************************************************************************
    def body(self, data):
        """ Encode HTTP POST body for dumeter.net API call """
        params = {}
        params['product'] = 'linux-dumeter-net-reporter'
        params['version'] = VERSION
        params['data'] = data
        params['moreinfo'] = ''
        return urllib.urlencode(params)

    # *****************************************************************************************************************
    def report(self, token, data):
        """ sent data (which is expected to already be in CSV format) to dumeter.net, using the given token """
        try:
            if not token: raise DuMeterError('Token is not set in the configuration file')
            request = urllib2.Request(self.url(token), self.body(data))
            handler = urllib2.urlopen(request)
            if handler.getcode() != 200:
                raise DuMeterError('Invalid reply from dumeter.net: %d' % handler.getcode())
            return True
        except IOError, e:
            logger.error('Reporting to dumeter.net has failed: %s', [str(e)])
            return False



# *****************************************************************************************************************
# *****************************************************************************************************************
# *****************************************************************************************************************
class RecordKeeper:
    """ This class keeps records in the database, for later submission to dumeter.net """

    # *****************************************************************************************************************
    def __init__(self):
        self.con = sqlite3.connect(config.database_file(), detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        self.con.row_factory = sqlite3.Row
        try:
            self.con.execute('CREATE TABLE config (version INTEGER)')
        except sqlite3.OperationalError:
            cur = self.con.execute('SELECT version FROM config')
            if (cur.fetchone()[0] == DB_VERSION):
                return
            else:
                raise DuMeterError('Invalid database version')
        # If we got here, it means new database is being created
        self.con.execute('CREATE TABLE IF NOT EXISTS stats (reporter STRING, dt TIMESTAMP, sent INTEGER default 0, recv INTEGER default 0,reported INTEGER default 0)')
        self.con.execute('CREATE UNIQUE INDEX IF NOT EXISTS stats_main ON stats (reporter,dt)')
        self.con.execute('INSERT INTO config (version) VALUES (?)', [DB_VERSION])
        self.con.commit()

    # *****************************************************************************************************************
    def current_hour(self):
        """ datetime of current hour, in UTC. """
        return datetime.datetime.utcnow().replace(minute=0, second=0, microsecond=0)

    # *****************************************************************************************************************
    def newdata(self, reporter, sent, recv):
        """ Add new record to the database """
        dt = self.current_hour()
        # Warning: this code is obviously not thread- or multi-process safe!
        # Make sure only one caller is modifying the database
        try:
            self.con.execute('INSERT or FAIL INTO stats (reporter,dt,sent,recv,reported) VALUES (?,?,?,?,0)', [reporter, dt, sent, recv])
        except sqlite3.IntegrityError:
            self.con.execute('UPDATE stats SET sent=sent+?, recv=recv+?, reported=0 WHERE reporter=? AND dt=?',[sent, recv, reporter, dt])
        self.con.commit()

    # *****************************************************************************************************************
    def csv_format(self, record):
        """ Format one database record for dumeter.net reporting (CSV format) """
        return '%s,%d,%d' % (record['dt'].isoformat(), record['sent'], record['recv'])

    # *****************************************************************************************************************
    def to_report(self, reporter):
        """ Get a list of all records to report, mark these records as being reported """
        one_year_ago = datetime.datetime.utcnow() + datetime.timedelta(-365)
        cur = self.con.execute('SELECT dt, sent, recv FROM stats WHERE reported<2 AND reporter = ? AND dt > ? ORDER BY dt', [reporter, one_year_ago])
        result = '\n'.join((self.csv_format(rec) for rec in cur))
        # Now, mark all these records as "being reported"
        self.con.execute('UPDATE stats SET reported=1 WHERE reported=0 AND reporter = ? AND dt > ?', [reporter, one_year_ago])
        self.con.commit()
        return result

    # *****************************************************************************************************************
    def update_reported(self, reporter, result):
        """ Update previously reported records as either successful report or failed report """
        if result:
            self.con.execute('UPDATE stats SET reported=2 WHERE reported=1 AND reporter = ?', [reporter])
        else:
            self.con.execute('UPDATE stats SET reported=0 WHERE reported=1 AND reporter = ?', [reporter])
        self.con.commit()



class Collector:
    # TODO: Support per-IP statistics from iptables counters, see: https://github.com/ldx/python-iptables

    def __init__(self):
        pass


setupLogging()

config = Config()
rep = DuMeterNetReporter()
rk = RecordKeeper()

rk.newdata('reporter1', 223424, 34534435345)
print rk.to_report('reporter1')
rep.report(config.dumeter_net_key('reporter1'),rk.to_report('test'))

# print rep.url(cfg.dumeter_net_key())

#data = []
#data.append(HourlyData(datetime.now(), 23423243, 234234))
#data.append(HourlyData(datetime.now(), 23423243, 234234))
#print '\n'.join((x.line() for x in data))



