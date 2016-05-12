#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: zhangrulun
# Date: 2016/5/12
# Function: Set the maintenance time for zabbix

import re
import sys
import json
import ssl
import urllib2
import time


def send_request_and_receive_response(url, data, header, operate):
    """
    Send the request and receive the response
    :param url:
    :param data:
    :param header:
    :param operate:
    :return:
    """
    request = urllib2.Request(url, data, header)
    try:
        result = urllib2.urlopen(request)
        if result:
            print "{operate} is successful!".format(operate=operate)
    except Exception as e:
        print "{operate} is failed! {error}".format(operate=operate, error=e)
    else:
        response = json.loads(result.read())
        result.close()
        return response


def get_auth_id_from_zabbix(url, header, user, pwd):
    """
    Get the auth id from zabbix
    :param url:
    :param header:
    :param user:
    :param pwd:
    :return:
    """
    data = json.dumps({
        "jsonrpc": "2.0",
        "method": "user.login",
        "params": {
            "user": user,
            "password": pwd
        },
        "id": 1
    })
    result = send_request_and_receive_response(url, data, header, "Auth")
    if result['result']:
        return result['result']


def set_maintenance_time(url, header, auth, maintence):
    """
    Update the maintenance info
    :param url:
    :param header:
    :param auth:
    :param maintence:
    :return:
    """
    data = json.dumps({
        "jsonrpc": "2.0",
        "method": "maintenance.update",
        "params": maintence,
        "auth": auth,
        "id": 2
    })
    result = send_request_and_receive_response(url, data, header, "Set the maintenance")
    if result:
        return result


def show_help():
    """
    Show the script help
    :return:
    """
    print "########################## Help #########################"
    print 'Format:python set_maintenance_time.py "start_date" period_length_unit period_length host_or_group'
    print 'start_date,the date of string.                  eg: "2016-05-12 14:30:00"'
    print "period_length_unit,value of min, hour or day.   eg: min"
    print "period_length,the param is depend on period_length_unit:"
    print "min                                       value:(5 - 59)"
    print "hour                                      value:(1 - 23)"
    print "day                                       value:(1 - 31)"
    print "host_or_group,the host id or group id.Separated by a colon between the host and id,ids separated by commas"
    print "eg: 'hostids:10005' or 'hostids:10005,16665' or 'groupids:2' or 'groupids:2,3'"
    print "Note:the 'hostids' and 'groupids' is the keyword,can not change!"
    print "########################## Help #########################"



def main():
    """
    The main function
    :return:
    """
    r_https = re.compile(r'https')

    # zabbix user info
    username = "Admin"
    password = "zabbix"

    # zabbix api url
    zabbix_api_url = "http://10.20.108.106/zabbix/api_jsonrpc.php"

    # Maintenance info
    maintenance_info = {
        "maintenanceid": 1,
        "name": "Temporary Maintenance",
        "active_till": 1521288300,
        "active_since": 1458212400
    }

    # header info for http
    header = {"Content-Type": "application/json"}

    # All host id or group id
    all_ids = []

    # when the url include https,set ssl._create_default_https_context = ssl._create_unverified_context
    if r_https.match(zabbix_api_url):
        ssl._create_default_https_context = ssl._create_unverified_context

    # Get all params form command line
    if len(sys.argv) == 5:
        try:
            # Get the start time of maintenance,change the time string to unit time
            start_date = int(time.mktime(time.strptime(sys.argv[1], "%Y-%m-%d %H:%M:%S")))
            period_length_unit = sys.argv[2]
            if period_length_unit == 'min':
                if int(sys.argv[3]) < 5:
                    print "Error:Incorrect maintenance period (minimum 5 minutes)"
                    exit(1)
                period_length = int(sys.argv[3]) * 60
            elif period_length_unit == "hour":
                period_length = int(sys.argv[3]) * 3600
            elif period_length_unit == "day":
                period_length = int(sys.argv[3]) * 86400
            host_or_group, ids = sys.argv[4].split(':')
            if ',' in ids:
                all_ids = ids.split(',')
            else:
                all_ids.append(ids)
            auth_id = get_auth_id_from_zabbix(zabbix_api_url, header, username, password)
            maintenance_info["timeperiods"] = [{
                "start_date": start_date,
                "period": period_length
            }]
            maintenance_info[host_or_group] = all_ids
            result = set_maintenance_time(zabbix_api_url, header, auth_id,maintenance_info)
            print "Setting status:{status}".format(status=result)
        except Exception as e:
            print "Error:", e
            show_help()
    else:
        show_help()

if __name__ == '__main__':
    main()


