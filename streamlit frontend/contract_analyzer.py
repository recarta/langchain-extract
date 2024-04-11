import streamlit as st
import requests
import json

url = "http://localhost:8000"
USERID = "184D98E4-D2A8-4DE9-9430-D19479B51605"
extractors_headers = {"x-key": USERID, "Content-Type": "application/json", "Accept": "application/json"}
extractor_JSON_file = "../extractors/contract-type-extractor.json"
test_file = "../assets/test-material/test_workflow/LIMEENERGYCO_09_09_1999-EX-10-DISTRIBUTOR AGREEMENT.txt"

def load_extractor():
    request_data = open(extractor_JSON_file, "r").read()
    response = requests.post(f"{url}/extractors", data=request_data, headers=extractors_headers)
    print(response)
    if response.status_code == 200:
        response_json = json.loads(response.text)
        extractor_uuid = response_json["uuid"]
        return extractor_uuid
    else :
        return 0

def process_file():
    files = {
        'extractor_id': (None, st.session_state['extractor_UUID']),
        'file': ('filename.txt', open(test_file, 'rb')),
        'mode': (None, 'entire_document')
    }
    extract_headers = {"x-key": USERID,  "Accept": "application/json"}
    response = requests.post(f"{url}/extract", files=files, headers=extract_headers)
    print(response)
    if response.status_code == 200:
        print(response.text)
        response_json = json.loads(response.text)
        print(response_json)
        name = "not discovered yet"
        parties = response_json["data"][0]["parties"]
    else :
        name = "Contract Name: Not Found"
        parties = ["Party: Not Found"]
    return name, parties

# Streamlit UI components
st.title('Contract Analyzer')
if st.button('load extractor'):
    st.session_state['extractor_UUID']= load_extractor()
if 'extractor_UUID' in st.session_state:
    st.write(st.session_state['extractor_UUID'])
        
    #uploaded_file = st.file_uploader("Choose a contract file", type=['txt'])
    #if uploaded_file is not None:
        # Read the file (assuming text file for simplicity)
        # You might need to adjust this for other file types (PDF, DOCX, etc.)
        # file_content = uploaded_file.getvalue().decode("utf-8")

    if st.button('extract data'):
        # uploaded_file = open(test_file, "r").read()
        # Process the file
        name, parties = process_file()
        
        # Display the extracted data
        st.write(name)
        for party in parties:
            st.write(party)

else:
    st.write("Extractor not loaded")
