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
# See this page for more info on abstract python classes:
# https://julien.danjou.info/blog/2013/guide-python-static-class-abstract-methods
#
#****************************************************************************

#****************************************************************************
# Imports
#****************************************************************************
# python standard imports

# project-specific imports
from abstractCheck import AbstractCheck
from hooksterExceptions import *
from logManager import *

#****************************************************************************
# Constants
#****************************************************************************

#****************************************************************************
# Functions
#****************************************************************************

#****************************************************************************
# Classes
#****************************************************************************


class CheckRejectTabs(AbstractCheck):

    def __init__(self, config, check_name, check_config_dict):
        """
        Initialize this check
        """
        super(type(self), self).__init__(config, check_name, check_config_dict)

    def check_file(self, file_obj):
        """
        Run this check against the file_obj parameter

        This method should raise a CheckException if the check fails
        """

        if file_obj.contents is None:
            # this file is empty.  (It's likely being deleted).  obviously we don't need to check
            # for tabs
            return

        log("Running " + self.check_name + " on " + file_obj.filename)
        if file_obj.contents.find("\t") != -1:
            raise CheckException("File " + file_obj.filename + " contains tabs.  Replace tabs with spaces and re-commit.")

