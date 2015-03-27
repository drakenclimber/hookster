#!/usr/bin/env python
#****************************************************************************
# &copy;
# Copyright 2014-2015 Tom Hromatka
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#****************************************************************************

#****************************************************************************
# Imports
#****************************************************************************
# python standard imports
import ConfigParser
import importlib
import inspect

# project-specific imports
import configManager
import hooksterExceptions
from logManager import *

#****************************************************************************
# Constants
#****************************************************************************

OPTION_CHECKS_ENABLED = "checks_enabled"
OPTION_EXTENSIONS = "extensions"

#****************************************************************************
# Functions
#****************************************************************************

#****************************************************************************
# Classes
#****************************************************************************


class ConfigCheckManager(object):
    """
    Configuration manager for Checks class
    """

    def __init__(self, config):
        """
        Initialize this instance of the ConfigCheckManager
        :param config - ConfigManager instance
        """

        self.config = config

        # read in the checks and their configurations
        self.checks = self.get_checks()

        self.check_options = {}
        self.check_objs = {}
        for check in self.checks:
            self.check_options[check] = self._build_check_dict(check)
            self.check_objs[check] = self._import_check(check)

    def _build_check_dict(self, check_name):
        """Given a check name, read its config section and generate a python dictionary of its options"""

        try:
            # the config.items() call returns data in a two-dimensional python list
            # e.g. given a config line such as:
            # Extensions=*.py,*.java,*.c
            # the config.items() call will return 
            #  [('extensions', '*.py,*.java,*.c')]
            option_list  = self.config.get_section(check_name)
        except ConfigParser.NoSectionError:
            raise hooksterExceptions.ConfigException("%s does not have a section in %s" % (check_name, self.config.config_file))

        check_dict = {}
        #self.check_options[check_name] = {}
        for option in option_list:
            # see the comment above for parsing the return of config.items()
            check_dict[option[0]] = option[1]
            #self.check_options[check_name][option[0]] = option[1]

        for key in check_dict.keys():
            log("check_options[%s] = %s" % (key, check_dict[key]), LOG_LEVEL_TRACE)

        return check_dict

    def _import_check(self, check_name):
        """
        Given a check name, import and return the instance of it
        """

        module = importlib.import_module(check_name)

        # loop through the objects in this module
        for name, obj in inspect.getmembers(module):

            # we have found a concrete class.  instantiate it
            if inspect.isclass(obj) and not inspect.isabstract(obj) and name == check_name:

                # get the class
                check_class = getattr(module, name)

                # instantiate it
                check_instance = check_class(self.config, check_name, self.check_options[check_name])

                return check_instance

        # we should never get here.  there was a problem importing the check
        raise hooksterExceptions.CheckException("Could not import check: " + check_name)

    def get_checks(self):
        checks = self.config.get_option(OPTION_CHECKS_ENABLED).split(",")

        return checks

    def get_check_extensions(self, check_name):
        """Given a check name, return the extensions it is to be run on"""

        try:
            extensions = self.config.get_option(OPTION_EXTENSIONS, check_name).split(',')
        except ConfigParser.NoOptionError:
            # this check didn't define an extensions options.  Return "*"
            log("WARNING: " + check_name + " did not define an \'extensions\' section in the config file.  Using \'*\'",
                LOG_LEVEL_ERROR)
            extensions = "*"

        return extensions
