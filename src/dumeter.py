#!/usr/bin/python -Es
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

import sys
import time
import argparse
import dumeter
from dumeter.config import Config
from dumeter.recordkeeper import RecordKeeper
from dumeter.reporter import Reporter
from dumeter.logger import logger

# setproctitle is nice, but optional.
try:
    from setproctitle import setproctitle
except:
    def setproctitle(title):
        pass

if __name__ == "__main__":
    setproctitle(dumeter.NAME)
    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str, nargs='?', default=dumeter.DEFAULT_CONF_PATH, help='configuration file location')
    args = parser.parse_args()
    # Start the program
    logger().info('%s %s is starting.' % (dumeter.NAME, dumeter.VERSION))
    config = Config(args.config)
    recordkeeper = RecordKeeper(config)
    reporters = [Reporter(config, recordkeeper, name) for name in config.reporters()]
    report_counter = dumeter.REPORT_FREQUENCY # send report immediately after startup
    if len(reporters) < 1:
        logger().critical('No reporters are defined in the config file %s, nothing to do!', config.path)
        sys.exit(1)
    logger().info('%s %s has started successfully.' % (dumeter.NAME, dumeter.VERSION))
    try:
        # Rationale: we're running either under systemd or upstart, and both can manage daemons
        # No need to keep daemonizing code in the application itself, everything is done here and no forking.
        # We're relying on systemd/upstart to close handles, etc.
        while 1:
            time.sleep(dumeter.SLEEP_BETWEEN_UPDATES)
            for reporter in reporters: reporter.update()
            report_counter += 1
            if report_counter >= dumeter.REPORT_FREQUENCY / dumeter.SLEEP_BETWEEN_UPDATES:
                report_counter = 0
                for reporter in reporters: reporter.send_report()
    except KeyboardInterrupt:
        sys.exit(0)

