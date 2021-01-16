import json
import sys

# Create the following files by refering to the samples.
csv_filename = "csv_file.csv"
central_filename = "input_credentials.json"

# Get instance of ArubaCentralBase from the central_filename
from pycentral.workflows.workflows_utils import get_conn_from_file, get_file_contents
input_args = get_file_contents(filename=central_filename)

# Get customer id from the central_filename
if "central_info" not in input_args:
    sys.exit("exiting... Provide central_info in the file %s" % central_filename)
central_info = input_args["central_info"]
customer_id = central_info['customer_id']

central = get_conn_from_file(filename=central_filename)

# Rename AP using the workflow `workflows.config_apsettings_from_csv.py`
from csv_overrides import gwSettingsCsv
gwSettingsCsv(conn=central, csv_filename=csv_filename, customer_id=customer_id)


