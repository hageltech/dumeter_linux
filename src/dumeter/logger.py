"""
    This file is part of dumeter.net network traffic reporter for Linux.
    Copyright (c) Copyright (c) 2014-2015 Hagel Technologies Ltd.

    This Source Code Form is subject to the terms of the Mozilla Public
    License, v. 2.0. If a copy of the MPL was not distributed with this
    file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

import sys
import logging
import logging.handlers
import dumeter

global_logger = None

# *****************************************************************************************************************
def setupLogging():
    """
     Set up logging for an application:
        1. Everything goes to Syslog.
        2. If STDOUT is a TTY, spit info there too.
    """
    logr = logging.getLogger(dumeter.NAME)
    logr.setLevel(logging.DEBUG)
    if sys.stdout.isatty():
        # Set up console logger if running in a console.
        cons = logging.StreamHandler()
        cons.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(levelname)s: %(message)s')
        cons.setFormatter(formatter)
        logr.addHandler(cons)
    # Set up the normal syslog logger
    syslog = logging.handlers.SysLogHandler(address='/dev/log', facility=logging.handlers.SysLogHandler.LOG_DAEMON)
    formatter = logging.Formatter('%(asctime)s %(name)s: %(levelname)s: %(message)s', '%b %e %H:%M:%S')
    syslog.setFormatter(formatter)
    logr.addHandler(syslog)
    return logr

# *****************************************************************************************************************
def logger():
    """ Convenience method to get the default logger in other modules. """
    global global_logger
    if global_logger is None:
        global_logger = setupLogging()
    return global_logger
