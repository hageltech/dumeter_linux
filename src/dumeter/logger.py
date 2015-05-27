
import dumeter
import sys
import logging
import logging.handlers

def setupLogging():
    logr = logging.getLogger(dumeter.NAME)
    logr.setLevel(logging.DEBUG)
    if sys.stdout.isatty():
        # Set up console logger if running in a console.
        cons = logging.StreamHandler()
        cons.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(levelname)s: %(message)s')
        cons.setFormatter(formatter)
        logr.addHandler(cons)
    # Set up normal syslog logger
    syslog = logging.handlers.SysLogHandler(address='/dev/log',facility=logging.handlers.SysLogHandler.LOG_DAEMON)
    formatter = logging.Formatter('%(asctime)s %(name)s: %(levelname)s: %(message)s', '%b %e %H:%M:%S')
    syslog.setFormatter(formatter)
    logr.addHandler(syslog)
    return logr

def logger():
    global global_logger
    if not ('global_logger' in globals()):
        global_logger = setupLogging()
    return global_logger
