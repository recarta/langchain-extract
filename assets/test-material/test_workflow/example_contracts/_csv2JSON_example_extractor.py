import csv
import json

# Path to your CSV file
csv_file_path = '_master_clauses.csv'

base_filenames= [
    "AURASYSTEMSINC_06_16_2010-EX-10.25-STRATEGIC ALLIANCE AGREEMENT",
    "CUROGROUPHOLDINGSCORP_05_04_2020-EX-10.3-SERVICING AGREEMENT",
    "LIMEENERGYCO_09_09_1999-EX-10-DISTRIBUTOR AGREEMENT",
    "SPIENERGYCO,LTD_03_09_2011-EX-99.5-OPERATIONS AND MAINTENANCE AGREEMENT",
    "SUCAMPOPHARMACEUTICALS,INC_11_04_2015-EX-10.2-STRATEGIC ALLIANCE AGREEMENT",
    "VARIABLESEPARATEACCOUNT_04_30_2014-EX-13.C-UNCONDITIONAL CAPITAL MAINTENANCE AGREEMENT"
]

csv_filename_extension = ".PDF"

interesting_keys = [
            "Document Name",
            "Parties",
            "Agreement Date",
            "Language",
        ]

for base_filename in base_filenames:
    # Initialize an empty dictionary to hold the CSV data
    temp_dict = {}
    csv_filename = f"{base_filename}{csv_filename_extension}"
    # Open the CSV file and read the data
    with open(csv_file_path, mode='r', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        # Read the first row and assign it as keys
        keys = next(csv_reader)
        
        for row in csv_reader:
            # Check if the first column in the row matches the constructed CSV filename
            if row[0] == csv_filename:
                # print("Found the row:", row)
                values = row
                break
        else:
            # This else block executes if the for loop completes without a break (i.e., no match found)
            print(f"##### No file named {csv_filename} found in the CSV.")
    # temp_dict holds the CSV data in a dictionary format
    temp_dict = dict(zip(keys, values))  

    # Modify the keys to match the expected JSON format for the extractor
    data_dict= {}
    for key in interesting_keys:
        data_dict[key] = temp_dict[f"{key}-Answer"]

    # Convert the dictionary to a JSON string
    json_data = json.dumps(data_dict, indent=4)

    # Optionally, print the JSON string to stdout
    # print(json_data)

    # Write the JSON string to a file
    output_json_file_name = f"{base_filename}_example.json"
    with open(output_json_file_name, 'w', encoding='utf-8') as jsonfile:
        jsonfile.write(json_data)