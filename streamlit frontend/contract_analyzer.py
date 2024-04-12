import streamlit as st
import requests
import json

url = "http://localhost:8000"
USERID = "184D98E4-D2A8-4DE9-9430-D19479B51605" #fixed for testing
extractors_headers = {"x-key": USERID, "Content-Type": "application/json", "Accept": "application/json"}
extractor_JSON_file = "../extractors/contract-type-extractor.json" #describe the JSON Schema for the extractor

#test file to extract data from
# there are 2 versions, the *light* one is better for testing 
test_file = "../assets/test-material/test_workflow/000000000_light.txt" 

#example files to train the extractor
example_folder = "../assets/test-material/test_workflow/example_contracts/"
example_files = [ 
        # "AURASYSTEMSINC_06_16_2010-EX-10.25-STRATEGIC ALLIANCE AGREEMENT",
        # "CUROGROUPHOLDINGSCORP_05_04_2020-EX-10.3-SERVICING AGREEMENT",
        "LIMEENERGYCO_09_09_1999-EX-10-DISTRIBUTOR AGREEMENT",
        "SPIENERGYCO,LTD_03_09_2011-EX-99.5-OPERATIONS AND MAINTENANCE AGREEMENT",
        "SUCAMPOPHARMACEUTICALS,INC_11_04_2015-EX-10.2-STRATEGIC ALLIANCE AGREEMENT",
        "VARIABLESEPARATEACCOUNT_04_30_2014-EX-13.C-UNCONDITIONAL CAPITAL MAINTENANCE AGREEMENT"
    ]


def train_extractor(extractorUUID):
    responses = []
    for example_file in example_files:
        example_file_path = f"{example_folder}/{example_file}.txt"
        example_file_example_data_path = f"{example_folder}{example_file}_example.json"
        filecontent = open(example_file_path, "r").read(800) # Read only the first 800 characters to avoid OpenAi limitations of token/minutes
        output = [json.loads(open(example_file_example_data_path, "r").read())]
        print(f"### Processing {example_file}")
        # print ("--------example_file_path = ", example_file_path)
        # print ("--------filecontent = ", filecontent)
        # print ("--------example_file_example_data_path = ", example_file_example_data_path)
        # print ("--------output = ", output)
        create_request = {
            "extractor_id": extractorUUID,
            "content": filecontent,
            "output": output,
        }
        response = requests.post(f"{url}/examples", json=create_request, headers=extractors_headers)
        # print(response.json())
        responses.append(response)
    # Check the number of examples loaded
    # response = requests.get(f"{url}/examples?extractor_id={extractorUUID}", headers=extractors_headers)
    # print("number of examples loaded:",len(response.json()))
    return response.json()

def create_extractor():
    request_data = open(extractor_JSON_file, "r").read()
    response = requests.post(f"{url}/extractors", data=request_data, headers=extractors_headers)
    if response.status_code == 200:
        response_json = json.loads(response.text)
        extractor_uuid = response_json["uuid"]
        train_extractor(extractor_uuid)
        return extractor_uuid
    else :
        return 0

def extract_file(filepath):
    files = {
        'extractor_id': (None, st.session_state['extractor_UUID']),
        'file': ('filename.txt', open(filepath, 'rb')),
        'mode': (None, 'entire_document')
    }
    extract_headers = {"x-key": USERID,  "Accept": "application/json"}
    response = requests.post(f"{url}/extract", files=files, headers=extract_headers)
    # print(response)
    if response.status_code == 200:
        response_json = json.loads(response.text)
        print(response_json)
        data =response_json["data"]
    else :
        data = [{
            "name" : "Contract Name: Not Found",
            "parties" : ["Not Found"],
        }]
    return data

def display_file_data (filepath):
     # Process the file
    data = extract_file(filepath)

    # for slice in data:
    slice = data[0]
    name = slice.get("name", "")    
    # Display the extracted data
    if name == "":
        name = st.text_input('Name', 'The name is missing. Please enter it manually.')
    else:
        st.write(name)
    st.write("Parties:")
    for party in slice["parties"]:
        st.write(party)
    

# Streamlit UI components
st.title('Contract Analyzer')
if st.button('load extractor'):
    st.session_state['extractor_UUID']= create_extractor()
if 'extractor_UUID' in st.session_state:
    st.write(st.session_state['extractor_UUID'])
        
    uploaded_file = st.file_uploader("Choose a contract file", type=['txt'])
    if uploaded_file is not None:
        display_file_data(uploaded_file)

    if st.button('extract data for test file'):
       display_file_data(test_file)

else:
    st.write("Extractor not loaded")
