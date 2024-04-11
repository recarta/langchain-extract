// Generate User_ID as secret key

USER_ID=$(uuidgen)
export USER_ID

// to create an extractor
    // /!\ /!\ 
    // Each "value" in the JSON-schema has to be less than 100 characters. Take a special care of the value of any "description" /!\
    // /!\ /!\ 

OUTPUT=$(curl -X 'POST' \
  'http://localhost:8000/extractors' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -H "x-key: ${USER_ID}" \
  -d "$(cat extractors/contract-type-extractor.json)")
echo $OUTPUT
extractor_UUID=$(echo "$OUTPUT" | jq -r '.uuid')
echo $extractor_UUID


//to send examples
    // /!\ /!\ 
    // Make sure the keys (and meanings) of the content of the example are in sync with the JSON schema /!\
    // Make sure you updated the UUID of the extractor /!\
    // /!\ /!\ 
curl -X POST "http://localhost:8000/examples" \
    -H "Content-Type: application/json" \
    -H "x-key: ${USER_ID}" \
    -d '{
          "extractor_id": ${extractor_UUID},
          "content": "$(cat assets/test-material/Test_workflow/LIMEENERGYCO_09_09_1999-EX-10-DISTRIBUTOR AGREEMENT_content.json)",
          "output": [
            "$(cat assets/test-material/test_workflow/LIMEENERGYCO_09_09_1999-EX-10-DISTRIBUTOR AGREEMENT_example.json)"
          ]
        }' | jq .


//to extract data from a txt file with the extractor
    // /!\ /!\ 
    // When transforming it to Python request, I was not able to send the text but I had to go through files  /!\
    // /!\ /!\ 
curl -s -X 'POST' \
'http://localhost:8000/extract' \
-H 'accept: application/json' \
-H 'Content-Type: multipart/form-data' \
-H "x-key: ${USER_ID}" \
-F 'extractor_id= ${extractor_UUID}' \
-F 'text= "$(cat assets/test-material/test_workflow/000000000.txt)"' \
-F 'mode=entire_document'

