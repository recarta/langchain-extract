// Generate User_ID as secret key

USER_ID=$(uuidgen)
export USER_ID

// to create an extractor
    // /!\ /!\ 
    // Each "value" in the JSON-schema has to be less than 100 characters. Take a special care of the value of any "description" /!\
    // /!\ /!\ 

curl -X 'POST' \
  'http://localhost:8000/extractors' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -H "x-key: ${USER_ID}" \
  -d "$(cat extractors/contract-type-extractor.json)"
//UUID of "contract-type-extractor" v1 0131853d-49b2-4eb2-a07f-9b152074a8e5

//to send examples
    // /!\ /!\ 
    // Make sure the keys (and meanings) of the content of the example are in sync with the JSON schema /!\
    // Make sure you updated the UUID of the extractor /!\
    // /!\ /!\ 
curl -X POST "http://localhost:8000/examples" \
    -H "Content-Type: application/json" \
    -H "x-key: ${USER_ID}" \
    -d '{
          "extractor_id": "0131853d-49b2-4eb2-a07f-9b152074a8e5",
          "content": "$(cat assets/test-material/Test_workflow/LIMEENERGYCO_09_09_1999-EX-10-DISTRIBUTOR AGREEMENT_content.json)",
          "output": [
            "$(cat assets/test-material/test_workflow/LIMEENERGYCO_09_09_1999-EX-10-DISTRIBUTOR AGREEMENT_example.json)"
          ]
        }' | jq .


//to extract data from a txt file with the extractor
curl -s -X 'POST' \
'http://localhost:8000/extract' \
-H 'accept: application/json' \
-H 'Content-Type: multipart/form-data' \
-H "x-key: ${USER_ID}" \
-F 'extractor_id=0131853d-49b2-4eb2-a07f-9b152074a8e5' \
-F 'text= "$(cat assets/test-material/test_workflow/000000000.txt)"' \
-F 'mode=entire_document'