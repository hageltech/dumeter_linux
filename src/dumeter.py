#!/usr/bin/env python

import dumeter
from dumeter.config import Config
from dumeter.recordkeeper import RecordKeeper
from dumeter.reporter import Reporter
from dumeter.logger import logger
import sys
import time
import argparse

# setproctitle is nice, but optional.
try:
    from setproctitle import setproctitle
except:
    def setproctitle(title):
        pass

def main():
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
        while 1:
            time.sleep(dumeter.SLEEP_BETWEEN_UPDATES)
            for reporter in reporters: reporter.update()
            report_counter += 1
            if report_counter >= dumeter.REPORT_FREQUENCY / dumeter.SLEEP_BETWEEN_UPDATES:
                report_counter = 0
                for reporter in reporters: reporter.send_report()
    except KeyboardInterrupt:
        sys.exit(0)

main()
