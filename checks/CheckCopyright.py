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

KEY_FIRST_LINE = "first_line"
KEY_LAST_LINE = "last_line"
KEY_COPYRIGHT_OWNER = "copyright_owner"

CHECK_TO_END_OF_FILE = -1
NOT_FOUND = -1

#****************************************************************************
# Functions
#****************************************************************************

#****************************************************************************
# Classes
#****************************************************************************


class CheckCopyright(AbstractCheck):

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

        log("Running " + self.check_name + " on " + file_obj.filename)

        current_year = time.strftime("%Y", time.localtime())
        hint = None

        if file_obj.contents is None:
            # this file is empty.  (It's likely being deleted).  we don't need to check
            # for copyright info
            return

        found_copyright = False
        for line_number, line in enumerate(file_obj.contents.splitlines()):
            if int(self.check_config_dict[KEY_LAST_LINE]) != CHECK_TO_END_OF_FILE and \
                line_number > int(self.check_config_dict[KEY_LAST_LINE]):
                # we have exceeded the "last_line".   exit the for loop
                break

            if line_number >= int(self.check_config_dict[KEY_FIRST_LINE]):
                if line.find("copyright") != NOT_FOUND or line.find("Copyright") != NOT_FOUND:
                    # this is likely the copyright line.  look for the current year and predicate

                    if not line.find(current_year) != NOT_FOUND:
                        hint = "Line %d contains 'copyright' but does not contain the current year" % (line_number + 1)
                        # go on to the next line in the file.  this was close but no cigar
                        continue

                    if not line.find(self.check_config_dict[KEY_COPYRIGHT_OWNER]) != NOT_FOUND:
                        hint = "Line %d contains 'copyright' but does not contain the correct copyright information\n" \
                               "Expected to find the copyright owner: %s" % \
                               (line_number + 1, self.check_config_dict[KEY_COPYRIGHT_OWNER])
                        # go on to the next line in the file.  this was close but no cigar
                        continue

                    # all of the copyright checks passed.  we have found the copyright string
                    found_copyright = True
                    break

        if not found_copyright:
            # we failed to find a valid copyright string, fail this check
            exception_string = "Failed to find the copyright line in %s" % file_obj.filename

            if hint is not None:
                exception_string += "\n%s" % hint

            raise CheckException(exception_string)
