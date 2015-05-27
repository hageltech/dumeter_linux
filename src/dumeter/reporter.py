
import dumeter
from dumeter.logger import logger
from dumeter.interfacecollector import InterfaceCollector
from dumeter.dumeter_net import DuMeterNetSender
import sys

class Reporter:
    """ This class integrates the collection/reporting that is done in other classes """

    # *****************************************************************************************************************
    def __init__(self, config, recordkeeper, name):
        self.name = name
        self.config = config
        self.recordkeeper = recordkeeper
        self.collector = InterfaceCollector(config.interface(self.name))
        if self.collector.device == None:
            logger().critical('Network interface name is not configured for reporter %s', name)
            sys.exit()
        if not (self.collector.device in InterfaceCollector.available_devices()):
            logger().warn('Network interface %s is not available for reporter %s' % (self.collector.device, name))

    # *****************************************************************************************************************
    def update(self):
        """ Collect network statistics, save them to the database """
        self.collector.update_stats()
        self.recordkeeper.newdata(self.name, self.collector.sent, self.collector.recv)

    # *****************************************************************************************************************
    def send_report(self):
        data = self.recordkeeper.to_report(self.name)
        if len(data) == 0:
            logger().warn('Nothing to report for reporter %s.' % self.name)
            return False
        sender = DuMeterNetSender()
        result = sender.report(self.config.dumeter_net_key(self.name), data)
        self.recordkeeper.update_reported(self.name, result)
        if result:
            logger().info('Reporting to dumeter.net for reporter %s was successful.', self.name)
        else:
            logger().error('Reporting to dumeter.net for reporter %s was unsuccessful.', self.name)
        return result
