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
import smtplib
import socket

# project-specific imports
from abstractAction import AbstractAction
from hooksterExceptions import *
from logManager import *

#****************************************************************************
# Constants
#****************************************************************************

KEY_SENDER = "sender"

KEY_SEND_TO_ON_FAILURE = "send_to_on_failure"
KEY_SEND_TO_ON_SUCCESS = "send_to_on_success"

KEY_FAILURE_SUBJECT = "failure_subject"
KEY_FAILURE_SUBJECT_PARAMS = "failure_subject_params"

KEY_FAILURE_BODY = "failure_body"
KEY_FAILURE_BODY_PARAMS = "failure_body_params"

KEY_SUCCESS_SUBJECT = "success_subject"
KEY_SUCCESS_SUBJECT_PARAMS = "success_subject_params"

KEY_SUCCESS_BODY = "success_body"
KEY_SUCCESS_BODY_PARAMS = "success_body_params"

#****************************************************************************
# Functions
#****************************************************************************

#****************************************************************************
# Classes
#****************************************************************************


class ActionEmail(AbstractAction):

    def __init__(self, config, action_name, action_config_dict):
        """
        Initialize this action
        """
        super(ActionEmail, self).__init__(config, action_name, action_config_dict)

    def _create_body(self, is_success):

        if is_success:
            template = self.action_config_dict[KEY_SUCCESS_BODY]
            params = self.action_config_dict[KEY_SUCCESS_BODY_PARAMS]
        else:
            template = self.action_config_dict[KEY_FAILURE_BODY]
            params = self.action_config_dict[KEY_FAILURE_BODY_PARAMS]

        return self.config.string_builder.build_string(template, params)

    def _create_mail(self, from_address, to_address, subject, body):
        return "From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n" % (from_address, to_address, subject) + body

    def _create_subject(self, is_success):

        if is_success:
            template = self.action_config_dict[KEY_SUCCESS_SUBJECT]
            params = self.action_config_dict[KEY_SUCCESS_SUBJECT_PARAMS]
        else:
            template = self.action_config_dict[KEY_FAILURE_SUBJECT]
            params = self.action_config_dict[KEY_FAILURE_SUBJECT_PARAMS]

        return self.config.string_builder.build_string(template, params)

    def _send_mail(self, sender, to_list, subject, body):
        server = smtplib.SMTP('localhost')
        server.set_debuglevel(0)

        for to_address in to_list.split(","):
            mail = self._create_mail(
                sender,
                to_address,
                subject,
                body)

            log(mail, LOG_LEVEL_DEBUG)
            server.sendmail(self.action_config_dict[KEY_SENDER], to_address, mail)

        server.quit()

    def run(self, is_success):
        """
        Run this action

        This method should raise an ActionException if the action fails
        """

        sender = self.action_config_dict[KEY_SENDER]
        subject = self._create_subject(is_success)
        body = self._create_body(is_success)

        if is_success:
            to_list = self.action_config_dict[KEY_SEND_TO_ON_SUCCESS]
        else:
            to_list = self.action_config_dict[KEY_SEND_TO_ON_FAILURE]

        self._send_mail(sender, to_list, subject, body)
