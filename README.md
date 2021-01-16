# SD-Branch automation

## General Information

The purpose of this repository is to build a set of automation scripts that could be applied to streamline operations around the deployment and maintenance of (Aruba) SD-Branch networks. While the use of these scripts for labs or production deployments is certainly encouranged, this should by no means considered official or supported software by Aruba, a Hewlett Packard Enterprise company. 

These scripts make use of several tools described in the [Aruba Developer Hub](https://developer.arubanetworks.com/aruba-central), which explains in much more precise terms that i'm capable of how external applications can interact with Aruba Central. Please check it out!


### Generic Requirements

As described in the developer hub, there are a certain set of steps you should go through in order to benefit from these scritps:
1. Follow the instructions on how to make use of the [API Gateway](https://developer.arubanetworks.com/aruba-central/docs/api-gateway) to get your Central account set up for remote access. 
1. Install [**pycentral**](https://github.com/aruba/pycentral), as these scripts make use of several of its modules.
1. Remember to edit the credentials files (several examples included) so your scripts can access Central.
1. Modify the scripts at will to suit your needs :)

## Scripts

### config_from_csv

This script is a bit of a proof of concept for bulk configurations. It takes a a CSV file with a set of gateway-specific overrides, and converts them to a set of commands that are pushed to Aruba Central's API gateway. For this particular example I've used local-fqdn attributes for IPsec tunnels in the example, but as long as we have the right CLI commands (as well as the right values in the CSV file, it would work in the same way.

#### Running the script

In order to run this script, first make sure you have all the key files in the right folder (list below). 
* csv_file.csv - this file should contain whatever device-specific attributes you want to push.
* run.py - this is what "runs" the show. It authenticates to central and calls the "worker" method.
* csv_overrides.py - this is the "worker" method, which goes through all the rows in the csv and pushes configs to central.
* input_credentials.json (option 1) - Use this file if you want the script to be capable of authenticating on its own. If we use this file, the app will refresh the token or even request a completely new one when needed.
* input_credentials.json (option 2) - Use this file if you prefer to generate the token in Central and just run the script once.

Then simply execute the run.py file, which takes care of triggering the full worflow.

#### Where do I get the csv file from?

This script is based on the premise that you will build your own csv file (provided you adapt the code in csv_overrides.py). But it doesn't hurt to have a starting point :)

What I've found to be the easiest is to go to Devices > Gateways either from "Global" or from any groups or labels you may be using. Then simply click on the "Download CSV" file on the right and reorder/remove the columns in excel.

![Obtain CSV](https://github.com/samuelperezbun/sd-branch-automation/blob/main/images/obtain-csv.png)



