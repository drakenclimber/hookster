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


class ActionException(Exception):
    """Exception to throw when an action fails"""
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return "[ACTION EXCEPTION] %s" % str(self.message)



class CheckException(Exception):
    """Exception to throw when a check fails"""
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return "[CHECK EXCEPTION] %s" % str(self.message)


class ConfigException(Exception):
    """Exception to throw when a invalid configuration file is provided"""
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return "[CONFIG EXCEPTION] %s" % str(self.message)


class ParameterException(Exception):
    """Exception to throw when a invalid parameter is provided"""
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return "[PARAM EXCEPTION] %s" % str(self.message)


class ScmException(Exception):
    """Exception to throw when there is an SCM error"""
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return "[SCM EXCEPTION] %s" % str(self.message)


class UnsupportedException(Exception):
    """Exception to throw when a feature is unsupported"""
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return "[UNSUPPORTED EXCEPTION] %s" % str(self.message)
