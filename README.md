# set_maintenance_time
Set the maintenance time for zabbix

You can set your zabbix info in the main function of set_maintenance_time.py


# change to your zabbix user
username = "Admin"
password = "zabbix"

# your zabbix api url
zabbix_api_url = "http://10.20.108.106/zabbix/api_jsonrpc.php"

# change to your maintenance info
maintenance_info = {
        "maintenanceid": 1,     # This is your maintenance id
        "name": "Temporary Maintenance",     # This is your maintenance name
        "active_till": 1521288300,           # The Validity is 2016/03/17 ~ 2018/03/17
        "active_since": 1458212400
    }
    
You can execute python set_maintenance_time.py for help

########################## Help #########################
Format:python set_maintenance_time.py "start_date" period_length_unit period_length host_or_group
start_date,the date of string.                  eg: "2016-05-12 14:30:00"
period_length_unit,value of min, hour or day.   eg: min
period_length,the param is depend on period_length_unit:
min                                       value:(1 - 59)
hour                                      value:(1 - 23)
day                                       value:(1 - 31)
host_or_group,the host id or group id.Separated by a colon between the host and id,ids separated by commas
eg: 'hostids:10005' or 'hostids:10005,16665' or 'groupids:2' or 'groupids:2,3'
Note:the 'hostids' and 'groupids' is the keyword,can not change!
########################## Help #########################
