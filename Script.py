# Import required modules
import urllib.request as ur
import json, pandas
from pandas import json_normalize
from datetime import datetime

# Specify the resource_id to be searched against
param_resource_id = '7e9e07d5-1aa2-4c5d-8981-23cae27dc674'
# Specify the maximum number of rows to return
param_limit = 1000
# Request URL
url = 'https://data.gov.sg/api/action/datastore_search?resource_id={}&limit={}'.format(param_resource_id, param_limit)
# Set a user agent as the default user agent specified by urllib.request.urlopen
# could be blocked to avoid web scrawlers
headers = {'User-Agent': 'Mozilla/5.0'}

# Access the data
request = ur.Request(url=url, headers=headers)
temp_file = open('temp.json', 'wb')
with ur.urlopen(request) as response:
    output = response.read()
    # Save the .json file to check the output
    temp_file.write(output)
    # Data to be cleaned
    data = json.loads(output.decode())

# Clean and transform the data
parent_node = 'result'
record_path = 'records'
# Remove unneeded info in the json output
table = json_normalize(data=data[parent_node], record_path=[record_path])
# Rename fields
table_renamed = table.rename(columns={
    "_id": "id",
    "financial_year": "Financial Year",
    "economic_sector": "Economic Sector",
    "no_of_businesses": "No. of Businesses",
    "percentage_of_businesses_in_net_gst_refund_position": "% of Businesses in Net GST Refund Position",
    "net_gst_contribution": "Net GST Contribution (S$ Thousand)",
    "percentage_of_net_gst_contribution": "% of Net GST Contribution"
})
# Check order of the fields in the json output
print(list(table_renamed.columns.values))
# Reorder fields
table_reordered = table_renamed[[
    'id',
    'Financial Year',
    'Economic Sector',
    'No. of Businesses',
    '% of Businesses in Net GST Refund Position',
    'Net GST Contribution (S$ Thousand)',
    '% of Net GST Contribution'
]]

# Save the cleaned json output into .csv file
# Specify the .csv file path and name
file_path = 'C:\\Users\\Xuan\\OneDrive - Nanyang Technological University\\Test\\GST by Economic Sector_'
# Name the .csv file with a date for Qlik Sense to identify and load the latest file
file_date = datetime.today().strftime("%Y%m%d")
table_reordered.to_csv(file_path + file_date + '.csv', index=False)
