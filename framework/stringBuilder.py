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
import time

# project-specific imports
from logManager import *

#****************************************************************************
# Constants
#****************************************************************************

OPTION_REPO_NAME = "repo_name"

#****************************************************************************
# Functions
#****************************************************************************

#****************************************************************************
# Classes
#****************************************************************************


class StringBuilder(object):
    """
    Class to create strings given a template and parameters
    """

    def __init__(self, config):
        """
        Initalize this class

        :param config: instantion of ConfigManager Python class
        :return: None
        """

        self.config = config

    def build_string(self, template, params):
        """
        Given a template and parameters, generate a string

        :param template: string template, e.g. "It was a %s and %s night"
        :param params: comma-separated list of parameters, e.g. "dark,stormy"
        :return: The evaluated string, e.g. "It was a dark and stormy night"
        """

        out_string = None

        log("build_string() template == %s" % template, LOG_LEVEL_TRACE)

        if len(params.strip()):
            log("build_string() params == %s" % params, LOG_LEVEL_TRACE)
            param_string = self.parse_params(params)
            log("build_string() param_string == %s" % param_string, LOG_LEVEL_TRACE)

            eval_string = "%s %% (%s)" % (template, param_string)
            out_string = (eval(eval_string))
        else:
            # the param list is empty.  simply return the template
            out_string = template

        return out_string

    def parse_params(self, params):
        """
        Given a list of parameters (from the hookster config file), parse and convert them to a format we can eval()
        """
        param_list = []

        for param in params.split(","):
            if param == "author":
                param_list.append("'%s'" % self.config.scm.get_author(self.config.new_rev))

            elif param == "branch_name":
                param_list.append("'%s'" % self.config.branch_name)

            elif param == "branch_basename":
                param_list.append("'%s'" % self.config.branch_basename)

            elif param == "commit_id":
                param_list.append("'%s'" % self.config.new_rev)

            elif param == "date_time":
                date_time_str = time.strftime(time_format, time.localtime())
                param_list.append("'%s'" % date_time_str)

            elif param == "file_list":
                file_list = self.config.scm.get_changed_file_list(self.config.new_rev)
                file_list_str = "\\n".join(file_list)
                param_list.append("'%s'" % file_list_str)

            elif param == "new_rev":
                param_list.append("'%s'" % self.config.new_rev)

            elif param == "old_rev":
                param_list.append("'%s'" % self.config.old_rev)

            elif param == "patch":
                raise UnsupportedException("Currently not supported.  It was too easy to confuse python with complex patches")

                patch = self.config.scm.generate_commit_patch(self.config.new_rev, self.config.old_rev)
                param_list.append("'%s'" % patch)

            elif param == "repo":
                param_list.append("'%s'" % self.config.get_option(OPTION_REPO_NAME))

            elif param == "scm_browser_url":
                param_list.append("'%s'" % self.config.scm_browser_url)

            else:
                raise ActionException("Invalid parameter: " + param)

        return ",".join(param_list)
