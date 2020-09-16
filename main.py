#! usr/bin/env python

import os
import json
import requests
from requests.auth import HTTPBasicAuth

if __name__ == '__main__':

    auth = HTTPBasicAuth('admin','admin123')

    headers = {
            'Content-Type': 'application/json'
    }

    params = {
            'query' : 'SELECT SysName FROM Orion.Nodes'
    }

    requests.packages.urllib3.disable_warnings()

    url = "https://10.33.158.246:17778/SolarWinds/InformationService/v3/Json/Query"

    response = requests.get(url, auth=auth, headers=headers, params=params ,verify=False)

    result = json.loads(response.text)

# Get a sorted list of SysName out of the list of dictionaries in "results"

    sw_data = sorted([d['SysName'][0:8] for d in result['results']])

    print 'This is the info from SW:   \n', sw_data


# Get list from the achive server

    cmd = 'ls -1 /home/wilfredo/logs_test | cut -c 1-8 | sort | uniq | sed "s/[a-z]/\U&/g"'

    opt = os.popen(cmd).read()

    ar_data = opt.split('\n')

    print 'This is the info from AR Server:   \n', ar_data

# Compare and give the differences

    diff = set(sw_data).symmetric_difference(set(ar_data))

    list_diff = list(diff)

    print 'This is the difference between systems: ', list_diff
