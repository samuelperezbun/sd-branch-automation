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

This script takes a CSV file with a set of gateway-specific overrides and converts them to a set of commands that are pushed through Aruba Central's API gateway. 

