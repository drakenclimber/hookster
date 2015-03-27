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
import sys
import traceback

# project-specific imports
cur_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(cur_path, 'actions'))
sys.path.append(os.path.join(cur_path, 'checks'))
sys.path.append(os.path.join(cur_path, 'framework'))
sys.path.append(os.path.join(cur_path, 'scm'))

import abstractScm
from configManager import ConfigManager
from fileObject import FileObject
from hooksterExceptions import *
from logManager import *

#****************************************************************************
# Constants
#****************************************************************************
CONFIG_FILE = os.path.join(cur_path, "hookster.conf")

#****************************************************************************
# Functions
#****************************************************************************

def setup(config_file, scm, old_rev, new_rev, branch):
    """Setup hookster"""

    config = ConfigManager(config_file, scm, old_rev, new_rev, branch)

    return config

def teardown():
    """Teardown hookster"""

    close_log()

def run_this_check(config, check_name, filename):
    """Returns True if this check is to be run on this file"""

    run_check = False
    extension_list = config.check.get_check_extensions(check_name)
    file_extension = "*" + os.path.splitext(filename)[1] 

    if file_extension in extension_list:
        # This extension is in the whitelist.  We need to run this check on this file
        run_check = True

    return run_check

def main(config_file, scm, old_rev, new_rev, branch):
    """
    Hookster entry point

    :param scm:
    :param old_rev:
    :param new_rev:
    :param branch:
    :return: None
    """

    try:
        config = setup(config_file, scm, old_rev, new_rev, branch)

        # loop through each modified file
        for filename in config.scm.get_changed_file_list(config.new_rev):
            file_object = FileObject(filename, config.scm, config.branch_name, config.new_rev, config.old_rev)

            # loop through the enabled checks
            for check in config.check.checks:
                if run_this_check(config, check, file_object.filename):
                    config.check.check_objs[check].check_file(file_object)

        # all checks passed.  run the "success" actions.
        for key in config.action.success_action_objs.keys():
            config.action.success_action_objs[key].run(True)

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        log(message, LOG_LEVEL_ERROR)

        backtrace = traceback.format_exc()
        log(backtrace, LOG_LEVEL_ERROR)

        # run the "failed" actions
        for key in config.action.failure_action_objs.keys():
            config.action.failure_action_objs[key].run(False)

        # re-raise the failing exception
        raise

    finally:
        teardown()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Hookster - software configuration management hook scripts")

    parser.add_argument('-s', '--scm', dest='scm', default=abstractScm.SCM_DEFAULT, type=str,
                        help='SCM type, e.g. git, svn, etc.')
    parser.add_argument('-o', '--oldrev', dest='old_rev', default=None, type=str,
                        help='Hash/ID that represents the previous (old) revision')
    parser.add_argument('-n', '--newrev', dest='new_rev', default=None, type=str,
                        help='Hash/ID that represents the incoming (new) revision')
    parser.add_argument('-b', '--branch', dest='branch', default=None, type=str,
                        help='Branch name')
    parser.add_argument('-c', '--config', dest='config_file', default=CONFIG_FILE, type=str,
                        help='Hookster configuration file')

    args = parser.parse_args()

    sys.exit(main(args.config_file, args.scm, args.old_rev, args.new_rev, args.branch))
