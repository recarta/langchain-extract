import csv
import json

# Path to your CSV file
csv_file_path = 'LIMEENERGYCO_09_09_1999-EX-10-DISTRIBUTOR AGREEMENT.csv'
output_json_file_name = 'LIMEENERGYCO_09_09_1999-EX-10-DISTRIBUTOR AGREEMENT_example.json'

# Initialize an empty dictionary to hold the CSV data
data_dict = {}

# Open the CSV file and read the data
with open(csv_file_path, mode='r', encoding='utf-8') as csvfile:
    # Create a CSV reader
    csv_reader = csv.reader(csvfile, delimiter=',')
    # Read the first row and assign it as keys
    keys = next(csv_reader)
    # Read the second row and assign it as values
    values = next(csv_reader)

# Modify the keys to match the expected JSON format for the extractor
modified_keys = [k if k == "Filename" else k.replace("-Answer", "") if k.endswith("-Answer") else k + "-Tip" for k in keys]

# Map keys to values
data_dict = dict(zip(modified_keys, values))

# Convert the dictionary to a JSON string
json_data = json.dumps(data_dict, indent=4)

# Optionally, print the JSON string to stdout
print(json_data)

# Optionally, write the JSON string to a file
with open(output_json_file_name, 'w', encoding='utf-8') as jsonfile:
    jsonfile.write(json_data)