
# encoding = utf-8

import os
import sys
import time
import datetime
import requests
import json
from datetime import datetime, timedelta

'''
    IMPORTANT
    Edit only the validate_input and collect_events functions.
    Do not edit any other part in this file.
    This file is generated only once when creating the modular input.
'''
'''
# For advanced users, if you want to create single instance mod input, uncomment this method.
def use_single_instance_mode():
    return True
'''


def validate_input(helper, definition):
    """Implement your own validation logic to validate the input stanza configurations"""
    # This example accesses the modular input variable
    # base_url = definition.parameters.get('base_url', None)
    # username = definition.parameters.get('username', None)
    # api_token = definition.parameters.get('api_token', None)
    # from = definition.parameters.get('from', None)
    # to = definition.parameters.get('to', None)
    # offset = definition.parameters.get('offset', None)
    # limit = definition.parameters.get('limit', None)
    # filter = definition.parameters.get('filter', None)
    start_time = definition.parameters.get('from', None)
    try:
        datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S')
    except ValueError:
        raise ValueError(
            "Incorrect data format, time should be YYYY-MM-DDThh:mm:ss")
    pass


def collect_events(helper, ew):
    """
    Implement your data collection logic here
    """
    opt_base_url = helper.get_arg('base_url')
    opt_username = helper.get_arg('username')
    opt_api_token = helper.get_global_setting('api_token')
    opt_from = helper.get_arg('from')

    # create checkpoint key
    key = helper.get_input_stanza_names() + "_processing"

    # check checkpoint
    helper.log_debug("[-] JIRA Audit Log : check checkpoint")

    helper.log_debug("check_point: {}".format(
        helper.get_check_point(key)))

    start_time = helper.get_check_point(key)
    if start_time is None:
        start_time = opt_from
        helper.save_check_point(key, opt_from)
    else:
        # shift the starttime by 1 second
        start_time = (datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S') +
                      timedelta(seconds=1)).strftime('%Y-%m-%dT%H:%M:%S')

    helper.log_debug("[-] JIRA Audit Log : Start Time: {}".format(start_time))

    offset = 0
    opt_limit = 1000
    records = opt_limit
    while(records == opt_limit):       
        records = get_audit_logs(opt_username, opt_api_token, opt_base_url,
                                start_time, offset, opt_limit, ew, helper, key)
        if records:
            offset = offset + records


def build_url(base_url, start, offset, limit):
    endpoint = "/rest/api/3/auditing/record"
    param = "?from=" + str(start)
    if offset:
        param += "&offset=" + str(offset)
    if limit:
        param += "&limit=" + str(limit)
    url = base_url + endpoint + param
    return url


def get_audit_logs(user, token, base_url, start, offset, limit, ew, helper, key):
    url = build_url(base_url, start, offset, limit)
    headers = {
        'Content-Type': 'application/json'
    }
    try:
        response = requests.get(url, auth=(user, token), headers=headers)
        helper.log_debug("[-] JIRA Audit Log API : Status Code from request URL: {} Status: {}".format(
            url, response.status_code))
        if response.status_code != 200:
            helper.log_debug(
                "\t[-] JIRA Audit Log API Error: {}".format(response.text))

        events = response.json()

        if "records" in events:
            for event in events["records"]:
                helper.log_debug(
                    "\t\t[-] JIRA Audit Log Event: {}".format(event))
                try:

                    event_time = event['created'][:-9]
                    event_epoch_time = (datetime.strptime(
                        event_time, '%Y-%m-%dT%H:%M:%S') - datetime(1970, 1, 1)).total_seconds()

                    helper.log_debug(
                        "Event Create Time: {} -- Epoch Time: {}".format(event_time, event_epoch_time))

                    ev = helper.new_event(data=json.dumps(event), time=event_epoch_time, host=None, index=None,
                                          source=None, sourcetype=helper.get_sourcetype(), done=True, unbroken=True)
                    ew.write_event(ev)

                    # save checkpoint for every event
                    timestamp = helper.get_check_point(key)

                    timestamp = max(datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S'), datetime.strptime(
                        event_time, '%Y-%m-%dT%H:%M:%S')).strftime('%Y-%m-%dT%H:%M:%S')
                    helper.save_check_point(key, timestamp)
                    helper.log_debug(
                        "[-] JIRA Audit Log Event: timestamp: {}".format(timestamp))
                    helper.log_debug(
                        "[-] JIRA Audit Log Event: Last run time saved: {}".format(helper.get_check_point(key)))

                except Exception as e:
                    helper.log_debug(
                        "\t[-] Try Block 2: JIRA Audit Log Event Exception {}".format(e))
        else:
            helper.log_debug("\t[-] No events to retrieve for {}.".format(url))

        if events["records"]:
            records_length = len(events["records"])
            return records_length
        else:
            helper.log_debug(
                "\t[-] No events to retrieve for {}. Response received: {}".format(url, events))
    except Exception as e:
        raise e
