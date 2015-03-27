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
import os

# project-specific imports
from abstractScm import AbstractScm
import abstractScm
from configActionManager import ConfigActionManager
from configCheckManager import ConfigCheckManager
import logManager
from scmGit import ScmGit
from stringBuilder import StringBuilder

#****************************************************************************
# Constants
#****************************************************************************

# Hookster section
SECTION_HOOKSTER = "Hookster"

# Options
OPTION_TIME_FORMAT = "time_format"
OPTION_SCM_BROWSER_URL = "scm_browser_url"
OPTION_SCM_BROWSER_URL_PARAMS = "scm_browser_url_params"

#****************************************************************************
# Functions
#****************************************************************************

#****************************************************************************
# Classes
#****************************************************************************


class ConfigManager(object):
    """
    Configuration manager class
    """

    def __init__(self, config_file, scm=abstractScm.SCM_DEFAULT, old_rev=None, new_rev=None, branch_name=None):
        """
        Initialize this instance of the ConfigManager
        :param config_file - string, full path and filename to the configuration file
        :param scm - string representing the SCM in use
        :param old_rev - commit id/hash string of the previous revision
        :param new_rev - commit id/hash string of the new revision
        :param branch_name - name of the branch that this commit applies to
        """

        self.config_file = config_file
        self.config = None
        self._parse_config_file()

        self.old_rev = old_rev
        self.new_rev = new_rev
        self.branch_name = branch_name
        self.branch_basename = os.path.basename(self.branch_name)

        if scm == abstractScm.SCM_GIT:
            self.scm = ScmGit(new_rev, old_rev)
        else:
            raise UnsupportedException("Unsupported SCM: " + scm)

        self.string_builder = StringBuilder(self)

        logManager.open_log(self)

        self.scm_browser_url = self.string_builder.build_string(
            self.get_option(OPTION_SCM_BROWSER_URL),
            self.get_option(OPTION_SCM_BROWSER_URL_PARAMS))

        # now that logging is initialized, populate the actions and checks
        self.check = ConfigCheckManager(self)
        self.action = ConfigActionManager(self)

    def _parse_config_file(self):
        """Parse the hookster configuration file"""

        self.config = ConfigParser.ConfigParser()
        self.config.read(self.config_file)

    def get_option(self, option, section=SECTION_HOOKSTER):
        """Given an option name, get its values"""
        return self.config.get(section, option)

    def get_section(self, section):
        """Get a list of name value pairs for the options in <section>"""

        return self.config.items(section)

    def get_time_format(self):
        """Get the time.strftime() format"""
        self.get_option(OPTION_TIME_FORMAT)
