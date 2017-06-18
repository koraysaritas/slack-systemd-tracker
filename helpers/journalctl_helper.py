#!/usr/bin/env python3
import re
import subprocess

from . import jentry
from . import slack_helper
from . import utils


def parse_journal_json(worker_store, journal_json):
    j = None

    syslog_identifier = journal_json[0]['SYSLOG_IDENTIFIER']
    message = journal_json[0]['MESSAGE']

    if syslog_identifier in worker_store.dict_target and worker_store.dict_target[syslog_identifier]:
        timestamp = utils.convert_timestamp(journal_json[0]['__REALTIME_TIMESTAMP'])
        hostname = journal_json[0]['_HOSTNAME']
        source_timestamp = utils.convert_timestamp(journal_json[0]['_SOURCE_REALTIME_TIMESTAMP'])

        j = jentry.JEntry()
        j.syslog_identifier = syslog_identifier
        j.message = message
        j.timestamp = timestamp
        j.hostname = hostname
        j.source_timestamp = source_timestamp

    return j


def try_match_pattern_or_keyword(pattern, message, is_keyword):
    m = None
    if is_keyword:
        m = re.match(pattern, message, re.IGNORECASE)
    else:
        m = re.match(pattern, message)
    return m


def process_jentry(slack_store, worker_store, j):
    is_found = False
    try:
        if j.syslog_identifier == "sshd":
            for match_item in worker_store.arr_of_dict_match:
                for key_match, dict_match in match_item.items():
                    is_active = dict_match["is-active"]
                    if is_active:
                        is_keyword = dict_match["is-keyword"]
                        pattern = dict_match["pattern"]
                        m = try_match_pattern_or_keyword(pattern, j.message, is_keyword)
                        if m:
                            is_found = True
                            if is_keyword:
                                j.notification_type = "keyword"
                                j.friendly_message = j.message

                            if key_match == "invalid-user":
                                j.notification_type = "login-fail"
                                username, ip_address = m.groups()
                                j.friendly_message = "invalid user {0}@{1} from {2}".format(username,
                                                                                            j.hostname,
                                                                                            ip_address)
                            elif key_match == "authentication-failure":
                                j.notification_type = "login-fail"
                                ip_address, username = m.groups()
                                j.friendly_message = "login failed {0}@{1} from {2}".format(username,
                                                                                            j.hostname,
                                                                                            ip_address)
                            elif key_match == "accepted-password":
                                j.notification_type = "login"
                                username, ip_address, port = m.groups()
                                j.friendly_message = "login {0}@{1} from {2} port {3}".format(username,
                                                                                              j.hostname,
                                                                                              ip_address, port)
                            elif key_match == "session-closed":
                                j.notification_type = "logout"
                                username = m.groups()[0]
                                j.friendly_message = "logout {0}@{1}".format(username, j.hostname)
        elif j.syslog_identifier == "sudo":
            is_found = True
            j.notification_type = "info"
            j.friendly_message = j.message
    except Exception as e:
        print("Exception @process_jentry: %s" % e)

    if is_found:
        slack_helper.slack_send_jentry_to_channel(slack_store, j)


def iter_journalctl():
    args = ['journalctl', '--since "5 minutes ago"', '-o', 'json']
    p = subprocess.Popen(args, stdout=subprocess.PIPE)
    return iter(p.stdout.readline, '')


def match_keyword(message, dict_keywords):
    if any(re.match(r, message, re.IGNORECASE) for k, r in dict_keywords.items()):
        return True
    return False
