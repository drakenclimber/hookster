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
import abc

# project-specific imports

#****************************************************************************
# Constants
#****************************************************************************

#****************************************************************************
# Functions
#****************************************************************************

#****************************************************************************
# Classes
#****************************************************************************


class AbstractCheck(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self, config, check_name, check_config_dict):
        """
        Initialize this check
        """
        self.config = config
        self.check_name = check_name
        self.check_config_dict = check_config_dict

    @abc.abstractmethod
    def check_file(self, file_obj):
        """
        Run this check against the file_obj parameter

        This method should raise a CheckException if the check fails

        :param config_dict - A dictionary containing the options for this check
        :param file_obj - An instance of fileObject
        :return - None
        """
