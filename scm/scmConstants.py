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

SCM_GIT = "git"
SCM_SVN = "svn"
SCM_DEFAULT = SCM_GIT

FILE_OP_ADDED = "Added"
FILE_OP_MODIFIED = "Modified"
FILE_OP_DELETED = "Deleted"
FILE_OP_UNKNOWN = "Unknown"

#****************************************************************************
# Functions
#****************************************************************************

#****************************************************************************
# Classes
#****************************************************************************


class AbstractScm(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def generate_file_patch(self, filename, new_commit_id, prev_commit_id):
        """
        Generate a patch for a given file

        :param filename - name of the file
        :param new_commit_id - hash or rev # of new commit
        :param prev_commit_id - hash or rev # of previous commit

        :return returns a string that contains the patch info of this commit
        """

    def generate_commit_patch(self, new_commit_id, prev_commit_id):
        """
        Generate a patch for new_commit_id

        :param new_commit_id - hash or rev # of new commit
        :param prev_commit_id - hash or rev # of previous commit

        :return returns a string that contains the patch info of this commit
        """

    @abc.abstractmethod
    def get_author(self, commit_id):
        """
        Given a commit id string, this function will return the author of the commit

        :param commit_id - string, ID/hash of the commit
        :return: - string, author
        """

    @abc.abstractmethod
    def get_changed_file_list(self, commit_id):
        """
        Given a commit id string, this function will return the list of changed files

        :param commit_id - string, ID/hash of the commit
        :return - a list of changed files
        """

    @abc.abstractmethod
    def get_file_contents(self, filename, commit_id):
        """
        Given a filename, get the entire contents of the file

        :param filename - name of the file to retrieve
        :param commit_id - string, ID/hash of the commit

        :return returns a string that contains the entire contents of the file
        """

    def get_file_operation(self, filename, commit_id):
        """
        Given a filename get the operation being performed on the file (add, modify, delete, etc.)

        :param filename - name of the file to retrieve
        :param commit_id - string, ID/hash of the commit

        :return returns a string that represents the operation being performed
        """
