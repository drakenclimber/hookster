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
from hooksterExceptions import *
from logManager import *

#****************************************************************************
# Constants
#****************************************************************************

OPTION_ACTIONS_ON_SUCCESS = "actions_on_success"
OPTION_ACTIONS_ON_FAILURE = "actions_on_failure"

#****************************************************************************
# Functions
#****************************************************************************

#****************************************************************************
# Classes
#****************************************************************************


class ConfigActionManager(object):
    """
    Configuration manager for Actions
    """

    def __init__(self, config):
        """
        Initialize this instance of the ConfigActionManager
        :param config - ConfigManager instance
        """

        self.config = config

        # read in the actions
        self.success_actions = self.get_actions(OPTION_ACTIONS_ON_SUCCESS)
        self.failure_actions = self.get_actions(OPTION_ACTIONS_ON_FAILURE)

        self.action_options = {}

        self.success_action_objs = {}
        for action in self.success_actions:
            self.action_options[action] = self._build_action_dict(action)
            self.success_action_objs[action] = self._import_action(action)

        self.failure_action_objs = {}
        for action in self.failure_actions:
            # it's possible we may doubly initialize an action dictionary, but that's cool
            self.action_options[action] = self._build_action_dict(action)
            self.failure_action_objs[action] = self._import_action(action)

    def get_actions(self, option):
        """
        Get the list of actions
        :param option: config option string
        :return: list of actions
        """
        actions = self.config.get_option(option)

        if len(actions.strip()) == 0:
            # no actions were specified.  return an empty list
            actions = []
        else:
            actions = actions.split(",")

        return actions

    def _build_action_dict(self, action_name):
        """Given a action name, read its config section and generate a python dictionary of its options"""

        try:
            # the config.items() call returns data in a two-dimensional python list
            # e.g. given a config line such as:
            # Extensions=*.py,*.java,*.c
            # the config.items() call will return
            #  [('extensions', '*.py,*.java,*.c')]
            option_list  = self.config.get_section(action_name)
        except ConfigParser.NoSectionError:
            raise hooksterExceptions.ConfigException("%s does not have a section in %s" % (action_name, self.config.config_file))

        action_dict = {}
        for option in option_list:
            # see the comment above for parsing the return of config.items()
            action_dict[option[0]] = option[1]

        for key in action_dict.keys():
            log("action_options[%s] = %s" % (key, action_dict[key]), LOG_LEVEL_TRACE)

        return action_dict

    def _import_action(self, action_name):
        """
        Given an action name, import and return the instance of it
        """

        module = importlib.import_module(action_name)

        # loop through the objects in this module
        for name, obj in inspect.getmembers(module):

            # we have found a concrete class.  instantiate it
            if inspect.isclass(obj) and not inspect.isabstract(obj) and name == action_name:

                # get the class
                action_class = getattr(module, name)

                # instantiate it
                action_instance = action_class(self.config, action_name, self.action_options[action_name])

                return action_instance

        # we should never get here.  there was a problem importing the action
        raise hooksterExceptions.ActionException("Could not import action: " + action_name)
