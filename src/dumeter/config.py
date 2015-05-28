"""
    This file is part of dumeter.net network traffic reporter for Linux.
    Copyright (c) Copyright (c) 2014-2015 Hagel Technologies Ltd.

    This Source Code Form is subject to the terms of the Mozilla Public
    License, v. 2.0. If a copy of the MPL was not distributed with this
    file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

import dumeter
import ConfigParser

class Config:
    """ Parses/reads configuration file, ensures sensible defaults """

    # *****************************************************************************************************************
    def __init__(self, path=None):
        self.config = ConfigParser.ConfigParser()
        if path == None: path = dumeter.DEFAULT_CONF_PATH
        self.path = path
        self.config.read(self.path)

    # *****************************************************************************************************************
    def reporters(self):
        """ List of all reporters in the config file """
        result = self.config.sections()
        if 'global' in result: result.remove('global')
        return result

    # *****************************************************************************************************************
    def dumeter_net_key(self, reporter):
        """ Key for a particular reporter """
        try:
            return self.config.get(reporter, 'link_code')
        except ConfigParser.Error:
            return None

    # *****************************************************************************************************************
    def interface(self, reporter):
        """ Interface to monitor for a particular reporter """
        try:
            return self.config.get(reporter, 'interface')
        except ConfigParser.Error:
            return None

    # *****************************************************************************************************************
    def database_file(self):
        """ Path to a database file """
        try:
            return self.config.get('global', 'database_file')
        except ConfigParser.Error:
            return dumeter.DEFAULT_DATABASE_PATH


