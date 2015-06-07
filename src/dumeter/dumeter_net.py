"""
    This file is part of dumeter.net network traffic reporter for Linux.
    Copyright (c) Copyright (c) 2014-2015 Hagel Technologies Ltd.

    This Source Code Form is subject to the terms of the Mozilla Public
    License, v. 2.0. If a copy of the MPL was not distributed with this
    file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

import urllib
import urllib2
import dumeter
from dumeter.logger import logger

class DuMeterNetSender(object):
    """ This class communicates with dumeter.net service """

    PREFIX = 'http://dumeter.net/token/data.csv?'

    # *****************************************************************************************************************
    def __url(self, token):
        """ Encode all needed parameters for dumeter.net URL """
        return self.PREFIX + urllib.urlencode({'token': token})

    # *****************************************************************************************************************
    def __body(self, data, moreinfo):
        """ Encode HTTP POST body for dumeter.net API call """
        params = {}
        params['product'] = 'du_linux'
        params['version'] = dumeter.VERSION
        params['data'] = data
        params['moreinfo'] = moreinfo
        return urllib.urlencode(params)

    # *****************************************************************************************************************
    def report(self, config, name, data):
        """ sent data (which is expected to already be in CSV format) to dumeter.net. """
        try:
            token = config.dumeter_net_key(name)
            moreinfo = "Interface: %s" % config.interface(name)
            if not token or (token == 'REPLACE-WITH-YOUR-DUMETER-NET-LINK-CODE'):
                raise dumeter.DuMeterError('link_code in configuration file is not set. See configuration file for instructions.')
            request = urllib2.Request(self.__url(token), self.__body(data, moreinfo))
            handler = urllib2.urlopen(request)
            if handler.getcode() != 200:
                raise dumeter.DuMeterError('Invalid reply from dumeter.net: %d' % handler.getcode())
            return True
        except IOError, exc:
            logger().error('Reporting to dumeter.net has failed: %s', [str(exc)])
            return False



