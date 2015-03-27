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
import argparse
import os

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


class FileObject(object):
    """
    Python class that represents a file
    """

    def __init__(self, filename, scm, branch_name, new_rev, old_rev):
        """Initialize this instance of a FileObject"""
        self.filename = filename
        self.branch_name = branch_name
        self.scm = scm
        self.relpath = None

        self.old_rev = old_rev
        self.new_rev = new_rev
        self.file_op = self.scm.get_file_operation(filename, new_rev)
        self.patch = self.scm.generate_file_patch(filename, new_rev, old_rev)
        self.contents = self.scm.get_file_contents(filename, new_rev, self.file_op)
