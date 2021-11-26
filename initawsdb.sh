aws dynamodb create-table \
--table-name Polls \
--attribute-definitions AttributeName=PK,AttributeType=S AttributeName=SK,AttributeType=S \
--key-schema AttributeName=PK,KeyType=HASH AttributeName=SK,KeyType=RANGE \
--provisioned-throughput ReadCapacityUnits=10,WriteCapacityUnits=10 \
--global-secondary-indexes \
"[
    {
        \"IndexName\": \"QueryIndex\",
        \"KeySchema\": [
            {\"AttributeName\":\"SK\",\"KeyType\":\"HASH\"},
            {\"AttributeName\":\"PK\",\"KeyType\":\"RANGE\"}
        ],
        \"Projection\": {
            \"ProjectionType\":\"ALL\"
        },
        \"ProvisionedThroughput\": {
            \"ReadCapacityUnits\":10,
            \"WriteCapacityUnits\":10
        }
    }
]" \
--endpoint-url http://localhost:8000

aws dynamodb put-item \
    --table-name Polls \
    --item '{ 
        "PK":{"S":"AUTHOR#reindeer"}, 
        "SK":{"S":"POLL#1"}, 
        "Question":{"S":"How are you doing?"},
        "Options":{"L":[
            {"M":{"option":{"S":"Good"}}},
            {"M":{"option":{"S":"Very good"}}},
            {"M":{"option":{"S":"Excellent"}}}
        ]}}' \
    --endpoint-url http://localhost:8000 \

aws dynamodb put-item \
    --table-name Polls \
    --item '{ 
        "PK":{"S":"AUTHOR#reindeer"}, 
        "SK":{"S":"POLL#2"}, 
        "Question":{"S":"Which of the following is NOT a computer programming language?"},
        "Options":{"L":[
            {"M":{"option":{"S":"Java"}}},
            {"M":{"option":{"S":"PHP"}}},
            {"M":{"option":{"S":"Microsoft"}}}
        ]}}' \
    --endpoint-url http://localhost:8000 \

aws dynamodb put-item \
    --table-name Polls \
    --item '{ 
        "PK":{"S":"AUTHOR#rye"}, 
        "SK":{"S":"POLL#3"}, 
        "Question":{"S":"What is the longest river in France?"},
        "Options":{"L":[
            {"M":{"option":{"S":"Loire"}}},
            {"M":{"option":{"S":"Seine"}}},
            {"M":{"option":{"S":"Gironde"}}},
            {"M":{"option":{"S":"Rhone"}}}
        ]}}' \
    --endpoint-url http://localhost:8000 

aws dynamodb put-item \
    --table-name Polls \
    --item '{ 
        "PK":{"S":"AUTHOR#rye"}, 
        "SK":{"S":"POLL#4"}, 
        "Question":{"S":"In which Australian state is Darwin?"},
        "Options":{"L":[
            {"M":{"option":{"S":"Queensland"}}},
            {"M":{"option":{"S":"Western Australia"}}},
            {"M":{"option":{"S":"Northern Territory"}}},
            {"M":{"option":{"S":"Tasmania"}}}
        ]}}' \
    --endpoint-url http://localhost:8000

aws dynamodb put-item \
    --table-name Polls \
    --item '{ 
        "PK":{"S":"AUTHOR#rye"}, 
        "SK":{"S":"POLL#5"}, 
        "Question":{"S":"What in America is the Palmetto state?"},
        "Options":{"L":[
            {"M":{"option":{"S":"Florida"}}},
            {"M":{"option":{"S":"Louisiana"}}},
            {"M":{"option":{"S":"Alabama"}}},
            {"M":{"option":{"S":"South Carolina"}}}
        ]}}' \
    --endpoint-url http://localhost:8000



