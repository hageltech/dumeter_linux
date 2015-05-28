"""
    This file is part of dumeter.net network traffic reporter for Linux.
    Copyright (c) Copyright (c) 2014-2015 Hagel Technologies Ltd.

    This Source Code Form is subject to the terms of the Mozilla Public
    License, v. 2.0. If a copy of the MPL was not distributed with this
    file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

__copyright__ = "Copyright (c) 2014-2015 Hagel Technologies Ltd."
__license__ = "MPL 2.0"
__email__ = "support@hageltech.com"

NAME = 'dumeter-reporter'
VERSION = '1.0b'
DB_VERSION = 1

DEFAULT_DATABASE_PATH = '/var/lib/' + NAME + '/db.sqlite'
DEFAULT_CONF_PATH = '/etc/' + NAME + '.conf'
REPORT_FREQUENCY = 120*60 # How often to report to dumeter.net, in seconds.
SLEEP_BETWEEN_UPDATES = 60 # How often to collect statistics, in seconds.
DEBUG = True

class DuMeterError(IOError):
    pass

