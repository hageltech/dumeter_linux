
import dumeter
from dumeter.logger import logger
import sys
import sqlite3
import datetime

class RecordKeeper:
    """ This class keeps records in the database, for later submission to dumeter.net """

    # *****************************************************************************************************************
    def __init__(self, config):
        try:
            self.con = sqlite3.connect(config.database_file(), detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        except sqlite3.OperationalError, e:
            logger().critical('Error opening database file "%s": %s', config.database_file(), str(e))
            sys.exit(1)
        self.con.row_factory = sqlite3.Row
        try:
            self.con.execute('CREATE TABLE config (version INTEGER)')
        except sqlite3.OperationalError:
            cur = self.con.execute('SELECT version FROM config')
            if (cur.fetchone()[0] == dumeter.DB_VERSION):
                return
            else:
                raise dumeter.DuMeterError('Invalid database version')
        # If we got here, it means new database is being created
        self.con.execute('CREATE TABLE IF NOT EXISTS stats (reporter STRING, dt TIMESTAMP, sent INTEGER default 0, recv INTEGER default 0,reported INTEGER default 0)')
        self.con.execute('CREATE UNIQUE INDEX IF NOT EXISTS stats_main ON stats (reporter,dt)')
        self.con.execute('INSERT INTO config (version) VALUES (?)', [dumeter.DB_VERSION])
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

