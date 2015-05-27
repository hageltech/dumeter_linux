
import dumeter
from dumeter.logger import logger
import urllib
import urllib2

class DuMeterNetSender:
    """ This class communicates with dumeter.net service """

    PREFIX = 'http://dumeter.net/token/data.csv?'

    # *****************************************************************************************************************
    def __url(self, token):
        """ Encode all needed parameters for dumeter.net URL """
        return self.PREFIX + urllib.urlencode({'token': token})

    # *****************************************************************************************************************
    def __body(self, data):
        """ Encode HTTP POST body for dumeter.net API call """
        params = {}
        params['product'] = 'linux-dumeter-net-reporter'
        params['version'] = dumeter.VERSION
        params['data'] = data
        params['moreinfo'] = ''
        return urllib.urlencode(params)

    # *****************************************************************************************************************
    def report(self, token, data):
        """ sent data (which is expected to already be in CSV format) to dumeter.net, using the given token """
        try:
            if not token: raise dumeter.DuMeterError('Token is not set in the configuration file')
            request = urllib2.Request(self.__url(token), self.__body(data))
            handler = urllib2.urlopen(request)
            if handler.getcode() != 200:
                raise dumeter.DuMeterError('Invalid reply from dumeter.net: %d' % handler.getcode())
            return True
        except IOError, e:
            logger().error('Reporting to dumeter.net has failed: %s', [str(e)])
            return False



