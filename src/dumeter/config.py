
import dumeter
import ConfigParser

class Config:
    """ Parses/reads configuration file, ensures sensible defaults """

    def __init__(self, path=None):
        self.config = ConfigParser.ConfigParser()
        if path == None: path = dumeter.DEFAULT_CONF_PATH
        self.path = path
        self.config.read(self.path)

    def reporters(self):
        """ List of all reporters in the config file """
        result = self.config.sections()
        if 'global' in result: result.remove('global')
        return result

    def dumeter_net_key(self, reporter):
        """ Key for a particular reporter """
        try:
            return self.config.get(reporter, 'link_code')
        except ConfigParser.Error:
            return None

    def interface(self, reporter):
        """ Interface to monitor for a particular reporter """
        try:
            return self.config.get(reporter, 'interface')
        except ConfigParser.Error:
            return None

    def database_file(self):
        """ Path to a database file """
        try:
            return self.config.get('global', 'database_file')
        except ConfigParser.Error:
            return dumeter.DEFAULT_DATABASE_PATH


