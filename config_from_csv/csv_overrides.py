# MIT License
#
# Copyright (c) 2020 Aruba, a Hewlett Packard Enterprise company
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""This workflow updates the local-fqdn of the tunnels configured to a cloud security provider. It uses (2 * N) number of API calls. 
where 'N' is the number of Gateways in the provided CSV file.
1. Read the user provided ".csv" file with the following format.
    ------------------------------------------------------------
    mac_address,group,hostname,1st-uplink-fqdn,2nd-uplink-fqdn, 3rd-uplink-fqd, 4th-uplink-fqdn
    00:11:22:33:44:55,group-001,gateway01,gateway01.uplink1,gateway01.uplink2,gateway01.uplink3,gateway01.uplink4
    01:11:22:33:44:66,group-002,gateway02,gateway02.uplink1,gateway02.uplink2,,gateway02.uplink3,gateway02.uplink4
    ------------------------------------------------------------
    * mac_address: The MAC Address of the gateway for which we'll define the uplink-fqdn values for the cloud security tunnels
    * group: The Aruba Central configuration group where the Gateway is located
    * hostname: The administrative name of the gateway. Mainly used for debugging purposes
    * 1st-uplink-fqdn: The local-fqdn that the gateway should use when establishing tunnels from the 1st uplink
    * 2nd-uplink-fqdn: The local-fqdn that the gateway should use when establishing tunnels from the 2nd uplink
    * 3rd-uplink-fqdn: The local-fqdn that the gateway should use when establishing tunnels from the 3rd uplink
    * 4th-uplink-fqdn: The local-fqdn that the gateway should use when establishing tunnels from the 4th uplink

   
2. For every GW in the csv file, obtain the settings to be used when forming tunnels to cloud security providers.
3. For every GW in the csv file, configure cloud security tunnels via API call based on the data obtained from Step2. 
3. Display a list of failed Gateways at end of the script.
"""

# Import Aruba Central Base and other functions
import os, sys
import csv
from pprint import pprint

from pycentral.base import ArubaCentralBase
from pycentral.base_utils import console_logger, parseInputArgs
from pycentral.workflows.workflows_utils import get_conn_from_file, get_file_contents

def gwSettingsCsv(conn, csv_filename: str, customer_id: str):
    """Function to configure tunnel settings.
    :param conn: Instance of class:`pycentral.ArubaCentralBase` to make an API call.
    :type conn: class:`pycentral.ArubaCentralBase` 
    :param csv_filename: Name of the CSV file in the format. To not modify some existing fields, leave it empty.
            mac_address,group,hostname,1st-uplink-fqdn,2nd-uplink-fqdn, 3rd-uplink-fqd, 4th-uplink-fqdn
            00:11:22:33:44:55,group-001,gateway01,gateway01.uplink1,gateway01.uplink2,gateway01.uplink3,gateway01.uplink4
            01:11:22:33:44:66,group-002,gateway02,gateway02.uplink1,gateway02.uplink2,,,

    :type csv_filename: str
    """    
    path = "/caasapi/v1/exec/cmd"

    with open(csv_filename, newline='') as csvfile:
        gateway_info = csv.DictReader(csvfile)
        for gateway_n in gateway_info:
            params = {
                "cid" : customer_id,
                "group_name" : gateway_n['group'] + "/" +  gateway_n['mac_address']
            }
            if gateway_n['1st-uplink-fqdn']:
                config_1st-uplink = {
                "cli_cmds" : [
                    "crypto-local ipsec-map cloud-security-uplink1 100",
                    "local-fqdn " + gateway_n['1st-uplink-fqdn'],
                    "!"
                    ]
                }
                conn.command(apiMethod="POST", apiPath=path, apiParams=params, apiData=config_1st-uplink)
                print("Pushed the following Config to Central:")
                pprint(config_1st-uplink)

            if gateway_n['2nd-uplink-fqdn']:
                config_2nd-uplink = {
                "cli_cmds" : [
                    "crypto-local ipsec-map cloud-security-uplink1 100",
                    "local-fqdn " + gateway_n['2nd-uplink-fqdn'],
                    "!"
                    ]
                }
                conn.command(apiMethod="POST", apiPath=path, apiParams=params, apiData=config_2nd-uplink)
                print("Pushed the following Config to Central:")
                pprint(config_2nd-uplink)
            #conn.command(apiMethod="POST", apiPath=path, apiParams=params, apiData=config_payload)


"""
Reminder:
mac_address = gateway_n['mac_address']
group = gateway_n['group']
hostname = gateway_n['hostname']
primary-uplink = gateway_n['1st-uplink-fqdn']
secondary-uplink = gateway_n['2nd-uplink-fqdn']
tertiary-uplink = gateway_n['3rd-uplink-fqdn']
quaternary-uplink = gateway_n['4th-uplink-fqdn']
"""