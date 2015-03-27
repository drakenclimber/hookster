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


class AbstractAction(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self, config, action_name, action_config_dict):
        """
        Initialize this action
        """
        self.config = config
        self.action_name = action_name
        self.action_config_dict = action_config_dict

    @abc.abstractmethod
    def run(self, is_success):
        """
        Run this action

        This method may raise an ActionException if the action fails

        :return - None
        """
