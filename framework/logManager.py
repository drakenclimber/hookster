#!/usr/bin/env python
#****************************************************************************
# &copy;
# Copyright 2015 Tom Hromatka
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
import time

# project-specific imports
from hooksterExceptions import *

#****************************************************************************
# Constants
#****************************************************************************

LOG_LEVEL_ERROR = 1
LOG_LEVEL_DEBUG = 2
LOG_LEVEL_TRACE = 3
LOG_LEVEL_DEFAULT = LOG_LEVEL_DEBUG

DEFAULT_LOG_FILE = None

LOG_SECTION = "Log"

KEY_DESTINATION = "destination"
KEY_LEVEL = "level"
KEY_FILE = "file"
KEY_FILE_PARAMS = "file_params"

OPTION_DESTINATION_FILE = "File"
OPTION_DESTINATION_SCREEN = "Screen"

#****************************************************************************
# Global Variables
#****************************************************************************

file_handle = None
log_level = LOG_LEVEL_DEFAULT
log_to_screen = False
time_format = "%Y-%m-%d %H:%M:%S"

#****************************************************************************
# Functions
#****************************************************************************

def _parse_and_validate_config(config):
    """
    Parse the "Log" section of the config file and validate it
    :param config: instantiation of the Python class ConfigManager
    :return: a dictionary of log settings
    """

    try:
        # the config.items() call returns data in a two-dimensional python list
        # e.g. given a config line such as:
        # Extensions=*.py,*.java,*.c
        # the config.items() call will return
        #  [('extensions', '*.py,*.java,*.c')]
        option_list  = config.get_section(LOG_SECTION)
    except ConfigParser.NoSectionError:
        option_list = None
        print("WARNING: Could not find 'Log' section in " + config.config_file)

    option_dict = {}
    for option in option_list:
        # see the comment above for parsing the return of config.items()
        option_dict[option[0]] = option[1]

    if len(option_dict) == 0:
        raise ConfigException("Log section shall not be empty.")

    if not KEY_LEVEL in option_dict:
        print(option_dict)
        raise ConfigException("Log section shall contain '%s' option." % KEY_LEVEL)

    if not KEY_FILE in option_dict:
        raise ConfigException("Log section shall contain '%s' option." % KEY_FILE)

    return option_dict

def _initialize_log_file(config, option_dict):
    """
    Initialize the log file handle (and other file settings) given a dictionary of settings
    from the config file
    :param option_dict: dictionary of log settings
    :return: Null
    """
    global file_handle

    if not OPTION_DESTINATION_FILE in option_dict[KEY_DESTINATION]:
        # we don't need to initialize the file logging (because the user didn't request it.)
        # bail out
        return

    # by getting to this point, we know that the user specified "File" in the "Destination" option.

    if option_dict[KEY_FILE] is None or option_dict[KEY_FILE] == "":
        raise ConfigException("A file must be specified when logging to a file.  Check your 'File=' option.")

    try:
        log_filename = config.string_builder.build_string(option_dict[KEY_FILE], option_dict[KEY_FILE_PARAMS])
        file_handle = open(log_filename, "w")
    except IOError:
        raise ConfigException("Couldn't open file, %s, for writing." % option_dict[KEY_FILE])

def _initialize_log_to_screen(option_dict):
    """
    Initialize the log to screen settings given a dictionary of settings from the config file
    :param option_dict: dictionary of log settings
    :return: Null
    """
    global log_to_screen

    if OPTION_DESTINATION_SCREEN in option_dict[KEY_DESTINATION]:
        log_to_screen = True

def _set_log_level(option_dict):
    """
    Set the log level
    :param option_dict: dictionary of log settings
    :return: Null
    """
    global log_level

    if option_dict[KEY_LEVEL] is None or option_dict[KEY_LEVEL] == "":
        log_level = LOG_LEVEL_DEFAULT
    else:
        log_level = int(option_dict[KEY_LEVEL])

def _set_time_format(config):
    global time_format

    time_format = config.get_time_format()

    if time_format is None:
        time_format = "%Y-%m-%d %H:%M:%S"

def open_log(config):
    global file_handle

    option_dict = _parse_and_validate_config(config)
    _initialize_log_file(config, option_dict)
    _initialize_log_to_screen(option_dict)
    _set_log_level(option_dict)
    _set_time_format(config)

def close_log():
    global file_handle

    if file_handle is not None:
        file_handle.close()

def log(message, level=LOG_LEVEL_DEFAULT):
    global log_level
    global file_handle
    global log_to_screen
    global time_format

    if level <= log_level:
        current_time = time.strftime(time_format, time.localtime())
        out_str = "%s: %s\n" % (current_time, message)

        # this message meets our logging threshold.  log it
        if file_handle is not None:
            file_handle.write(out_str)

        if log_to_screen:
            print(out_str)

def set_log_level(new_level=LOG_LEVEL_DEFAULT):
    global log_level

    log_level = new_level
