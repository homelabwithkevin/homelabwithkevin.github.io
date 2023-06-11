+++
author = "Kevin"
title = "Twilio SMS"
date = "2023-06-11"
description = "Designing Twilio Integration"
tags = [
    "twilio",
    "sms",
    "aws"
]
draft = true
+++

I use this basic architecture to text message myself what TV, Movies, and Books I've been enjoying.

{{<mermaid align="left" theme="neutral" >}}
graph LR
    sms --> Twilio --> Lambda --> DynamoDB
{{< /mermaid >}}

## Code
Get the latest code here: [GitHub](https://github.com/homelabwithkevin)

## Code Snippets
### lambda_function.py
```
import json
import base64
import time
from dynamodb import write

def lambda_handler(event, context):
    event_body = str((base64.b64decode(event['body'])), "utf-8")
    parsed_message = event_body.split("&")

    message_type, actual_message = None, None

    for m in parsed_message:
        equals = m.split('=')[0]
        if equals == 'From':
            # Removes the plus symbol.
            user = m.split('%2B')[1]

        if equals == 'Body':
            message = m.split('=')[1].replace("+"," ")
            split_message = message.split(' - ')
            message_type = split_message[0]
            actual_message = split_message[1]

    write(time.time(), message_type, actual_message, user)

    formatted_message_type = message_type.lower()

    if message_type == "TV":
        formatted_message_type = "tv episode"

    if message_type == "Book":
        formatted_message_type = "book"

    response_body = f"Enjoy that {formatted_message_type}!"

    result = {
        "statusCode": 200,
        "body": response_body
    }

    return result
```
    
### dynamodb.py
    
```
# This writes to the DynamoDB.
import boto3

def write(timestamp, message_type, actual_message, user):
    client = boto3.client('dynamodb')
    response = client.update_item(
        TableName="moveies-tv",
        Key={
            'id': {
                'S': str(timestamp)
            }
        },
        AttributeUpdates={
            'message_type': {
                'Value': {
                    'S': str(message_type)
                }
            },
            'actual_message': {
                'Value': {
                    'S': str(actual_message)
                }
            },
            'user': {
                'Value': {
                    'S': str(user)
                }
            }
        }
    )

    return response
```
