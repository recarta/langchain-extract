import streamlit as st
import requests
import json
import os
import pypandoc

url = "http://localhost:8000"
USERID = "184D98E4-D2A8-4DE9-9430-D19479B51605" #fixed for testing
extractors_headers = {"x-key": USERID, "Content-Type": "application/json", "Accept": "application/json"}
extractor_JSON_file = "../extractors/contract-type-extractor.json" #describe the JSON Schema for the extractor

#test file to extract data from
# there are 2 versions of the TXT file, the *light* one is shorter for testing 
test_TXT_file = "../assets/test-material/test_workflow/000000000.txt" 
test_DOCX_file = "../assets/test-material/test_workflow/ACCURAYINC_09_01_2010-EX-10.31-DISTRIBUTOR AGREEMENT.docx" 
test_PDF_file = "../assets/test-material/test_workflow/ALCOSTORESINC_12_14_2005-EX-10.26-AGENCY AGREEMENT.PDF" 

#example files to train the extractor
example_folder = "../assets/test-material/test_workflow/example_contracts/"
temp_transformation_folder = f'{example_folder}temp_transformation/'
example_files = [ 
        "AURASYSTEMSINC_06_16_2010-EX-10.25-STRATEGIC ALLIANCE AGREEMENT",
        "CUROGROUPHOLDINGSCORP_05_04_2020-EX-10.3-SERVICING AGREEMENT",
        "LIMEENERGYCO_09_09_1999-EX-10-DISTRIBUTOR AGREEMENT",
        "SPIENERGYCO,LTD_03_09_2011-EX-99.5-OPERATIONS AND MAINTENANCE AGREEMENT",
        "SUCAMPOPHARMACEUTICALS,INC_11_04_2015-EX-10.2-STRATEGIC ALLIANCE AGREEMENT",
        "VARIABLESEPARATEACCOUNT_04_30_2014-EX-13.C-UNCONDITIONAL CAPITAL MAINTENANCE AGREEMENT"
    ]

empty_data_slice = {
            "Document Name" : "Not Found",
            "Parties" : "Not Found",
            "Language": "Not Found",
            "Agreement Date": "Not Found"
        }

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

def extract_file(file_bytes):
    files = {
        'extractor_id': (None, st.session_state['extractor_UUID']),
        'file': file_bytes,
        'mode': (None, 'entire_document')
    }
    extract_headers = {"x-key": USERID,  "Accept": "application/json"}
    response = requests.post(f"{url}/extract", files=files, headers=extract_headers)
    if response.status_code == 200:
        response_json = json.loads(response.text)
        print(response_json)
        data =response_json["data"]
    else :
        print("**** Error in extract_file")
        print(response)
        data = [empty_data_slice]
    return data

def display_file_data (file_bytes):
     # Process the file
    data = extract_file(file_bytes)

    slice = data[0] #for long documents, the data is sliced in multiple parts. At first, I take the first slice
    
    for key in empty_data_slice.keys():
        value = slice.get(key, "")    #to prevent an Exception if the key is not found
        if value == "":   #if the key is not found, the value is set to "Not Found"
            value = st.text_input(key, f'The {key} is missing. Please enter it manually.')
        else:
            st.write(f"{key}:")
            st.write(value)    

    for key in set(slice.keys()) - set(empty_data_slice.keys()): #display the other keys in any order
        st.write(f"{key}:")
        st.write(slice[key])

def extract_DOCX_in_TXT(docx_path):
    docx_filename = os.path.basename(docx_path)
    print("docx_filename = ", docx_filename)
    txt_filename = docx_filename.replace(".docx", ".txt")
    txt_path = f'{example_folder}{txt_filename}'
    output = pypandoc.convert_file(docx_path, 'plain', outputfile=txt_path)
    if output == 0:
        print("Error in extract_DOCX_in_TXT")
        return 0
    return txt_path

# Streamlit UI components
st.title('Contract Analyzer')
if st.button('load extractor'):
    st.session_state['extractor_UUID']= create_extractor()
if 'extractor_UUID' in st.session_state:
    st.write(st.session_state['extractor_UUID'])
        
    uploaded_file = st.file_uploader("Choose a contract file", type=['txt','pdf','docx'])
    if uploaded_file is not None:
        if uploaded_file.name.endswith('.docx'):
            temp_docx_path = f'{temp_transformation_folder}{uploaded_file.name}'
            with open(temp_docx_path, 'wb') as f:
                f.write(uploaded_file.read())
            file_bytes = open(extract_DOCX_in_TXT(temp_docx_path), 'rb').read()
        else:
            file_bytes = uploaded_file.read()
        display_file_data(file_bytes)

    if st.button('extract data for test TXT file'):
       file_bytes = open(test_TXT_file, 'rb').read()
       display_file_data(file_bytes)

    if st.button('extract data for test PDF file'):
       file_bytes = open(test_PDF_file, 'rb').read()
       display_file_data(file_bytes)
    
    if st.button('extract data for test DOCX file'):
        file_bytes = open(extract_DOCX_in_TXT(test_DOCX_file), 'rb').read()
        display_file_data(file_bytes)

else:
    st.write("Extractor not loaded")
