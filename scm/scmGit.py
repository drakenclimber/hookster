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
import subprocess

# project-specific imports
from abstractScm import AbstractScm
import abstractScm
from hooksterExceptions import *
from scmConstants import *

#****************************************************************************
# Constants
#****************************************************************************

COMMAND_GIT = "git"

OPTION_SHOW = "show"
OPTION_DIFF = "diff"

LINE_AUTHOR = "Author:"
LINE_DIFF_GIT = "diff --git"

LINE_FILE_OP_ADDED = "new file"
LINE_FILE_OP_DELETED = "deleted"
LINE_FILE_OP_MODIFIED = "index"

LIST_GIT_SHOW = [COMMAND_GIT, OPTION_SHOW]
LIST_GIT_DIFF = [COMMAND_GIT, OPTION_DIFF]

#****************************************************************************
# Functions
#****************************************************************************

#****************************************************************************
# Classes
#****************************************************************************


class ScmGit(AbstractScm):
    def __init__(self, new_commit_id, prev_commit_id):
        """
        Initialize this class

        :param new_commit_id: hash of the new git commit
        :param prev_commit_id: hash of the previous git commit
        :return: None
        """

        self.name = abstractScm.SCM_GIT

        # cache some of the basic git calls we will use
        self.git_show = self._git_show(new_commit_id)
        self.git_diff = self._git_diff(new_commit_id, prev_commit_id)

    def _run(self, command):
        """Run a command"""

        proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out = proc.communicate()

        if proc.returncode != 0:
            raise ScmException("Error " + str(proc.returncode) + " running " + " ".join(command))

        std_out = out[0].decode('utf-8')
        std_err = out[1].decode('utf-8')

        return std_out, std_err

    def _git_show(self, hash):

        command = []
        command.append(COMMAND_GIT)
        command.append(OPTION_SHOW)
        command.append(hash)

        return self._run(command)

    def _git_diff(self, new_hash, prev_hash):

        command = []
        command.append(COMMAND_GIT)
        command.append(OPTION_DIFF)
        command.append(prev_hash)
        command.append(new_hash)

        return self._run(command)

    def _start_of_patch(self, line, filename):
        """
        Given a line and a filename, return true if this line is the start of the patch for filename

        :param filename: filename string
        :return: boolean
        """

        start_of_patch = False

        if line.startswith("diff --git"):
            if line.find("a/" + filename) != -1 and line.find("b/" + filename) != -1:
                start_of_patch = True

        return start_of_patch

    def _extract_file_diff(self, diff_std_out, filename):
        """
        Given a result from "git diff", extract the patch for the specified filename
        """
        patch_str = ""
        in_our_patch = False

        for line in diff_std_out.splitlines(False):
            if self._start_of_patch(line, filename):
                in_our_patch = True
            else:
                in_our_patch = False

            if in_our_patch:
                patch_str += line + "\n"

        return patch_str

    def generate_file_patch(self, filename, new_commit_hash, prev_commit_hash):
        """
        Given two commit hashes, generate the patch file for filename
        """

        if self.git_diff is None:
            std_out, std_err = self._git_diff(new_commit_hash, prev_commit_hash)
        else:
            # we cached the "git diff" command.  use the cached version
            std_out = self.git_diff[0]

        file_patch = self._extract_file_diff(std_out, filename)

        return file_patch

    def generate_commit_patch(self, new_commit_hash, prev_commit_hash):
        """
        Given two commit hashes, generate the patch file for the entire commit
        """

        if self.git_diff is None:
            std_out, std_err = self._git_diff(new_commit_hash, prev_commit_hash)
        else:
            # we cached the "git diff" command.  use the cached version
            std_out = self.git_diff[0]

        return std_out

    def get_changed_file_list(self, commit_id):
        """
        Given a commit hash, return the list of changed files

        From stackoverflow, the recommended git command is:
        git diff-tree --no-commit-id --name-only -r <commit_id>

        Another option:
        git show --name-only --pretty="format:" <commit_id>

        http://stackoverflow.com/questions/424071/list-all-the-files-for-a-commit-in-git
        """
        command = []
        command.append(COMMAND_GIT)
        command.append('diff-tree')
        command.append('--no-commit-id')
        command.append('--name-only')
        command.append('-r')
        command.append(commit_id)

        std_out, std_err = self._run(command)
        file_list = std_out.split()

        return file_list

    def get_file_contents(self, filename, commit_hash, file_op=None):
        """
        Given a filename and a commit, get the entire contents of the file.  Note that git (correctly)
        does not return the contents of deleted files.  Thus, the need for the file_op parameter.

        :param filename: filename string
        :param commit_hash: checkin hash
        :param file_op: operation being performed on this file (add, modify, delete)
        :return:
        """

        if file_op is None:
            file_op = self.get_file_operation(filename, commit_hash)

        file_contents = None

        if file_op != FILE_OP_DELETED:
            command = []
            command.append(COMMAND_GIT)
            command.append(OPTION_SHOW)
            command.append(commit_hash + ":" + filename)

            std_out, std_err = self._run(command)

            file_contents = std_out

        return file_contents

    def get_author(self, commit_hash):
        """
        Given a commit hash, return the author email address

        :param commit_hash: commit identifier
        :return: author's email address
        """

        command = []
        command.append(COMMAND_GIT)
        command.append(OPTION_SHOW)
        command.append("-s")
        command.append("--format=%cE")
        command.append(commit_hash)

        std_out, std_err = self._run(command)

        author_email = std_out.strip()

        return author_email

    def get_file_operation(self, filename, commit_hash):
        """
        Given a filename, get the operation (add, modify, delete) being performed on that file

        WARNING: Note that for large checkins, calling this for each file could be expensive.  An
                 optimization is to run "git show" once, then call this function for each file
                 in the commit change.

        :param filename: filename string
        :param commit_hash: commit in which this file was changed
        :return: scmConstants
        """

        file_op = FILE_OP_UNKNOWN

        if self.git_show is None:
            std_out, std_err = self._git_show(commit_hash)
        else:
            # use the cached git show
            std_out = self.git_show[0]

        in_our_patch = False
        for line in std_out.splitlines():
            if in_our_patch:
                in_our_patch = False

                if line.startswith(LINE_FILE_OP_ADDED):
                    file_op = FILE_OP_ADDED
                    break
                elif line.startswith(LINE_FILE_OP_DELETED):
                    file_op = FILE_OP_DELETED
                    break
                elif line.startswith(LINE_FILE_OP_MODIFIED):
                    file_op = FILE_OP_MODIFIED
                    break
                else:
                    raise ScmException("Unsupported file operation for filename, %s, in line %s." %
                                       (filename, line))

            if self._start_of_patch(line, filename):
                # this line signifies a new file in the commit
                # the next line will contain the file operation (add, modify, delete)
                in_our_patch = True

        return file_op
