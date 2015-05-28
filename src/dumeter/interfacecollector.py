"""
    This file is part of dumeter.net network traffic reporter for Linux.
    Copyright (c) Copyright (c) 2014-2015 Hagel Technologies Ltd.

    This Source Code Form is subject to the terms of the Mozilla Public
    License, v. 2.0. If a copy of the MPL was not distributed with this
    file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

import os
import dumeter
from dumeter.logger import logger

# TODO: Support per-IP statistics from iptables counters, see: https://github.com/ldx/python-iptables
# TODO: Support SNMP statistics of remote machines

class InterfaceCollector(object):
    """
        Collects rx/tx statistics for an interface
        Warning: this code is not portable, Linux-only.
    """

    sent_init = 0
    recv_init = 0
    sent = 0
    recv = 0
    device = ''

    STAT_SENT = 'tx_bytes'
    STAT_RECV = 'rx_bytes'

    # *****************************************************************************************************************
    @classmethod
    def available_devices(cls):
        """ Set of all available network devices """
        available = []
        for root, dirs, files in os.walk("/sys/devices"):
            if root.endswith("/net") and not root.endswith("/virtual/net"):
                available += dirs
        return set(available)

    def __init__(self, device):
        self.device = device
        # Double call zeroes the stats
        self.update_stats()
        self.update_stats()

    # *****************************************************************************************************************
    def __getstat(self, statname):
        """ Get network interface statistics """
        try:
            with open('/sys/class/net/%s/statistics/%s' % (self.device, statname)) as statfile:
                return int(statfile.read().strip())
        except IOError:
            return 0

    # *****************************************************************************************************************
    def update_stats(self):
        """ Update rx/tx network interface statistics for an interface """
        sent_new = self.__getstat(self.STAT_SENT)
        recv_new = self.__getstat(self.STAT_RECV)
        if sent_new < self.sent_init:
            self.sent_init = sent_new
        if recv_new < self.recv_init:
            self.recv_init = recv_new
        self.sent = sent_new - self.sent_init
        self.recv = recv_new - self.recv_init
        self.sent_init = sent_new
        self.recv_init = recv_new
        logger().debug('Updated stats for %s: sent=%d, recv=%d', self.device, self.sent, self.recv)
