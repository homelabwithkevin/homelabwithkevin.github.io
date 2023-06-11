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
+++

I use this basic architecture to text message myself what TV, Movies, and Books I've been enjoying.

{{<mermaid align="left" theme="neutral" >}}
graph LR
    sms --> Twilio --> Lambda --> DynamoDB
{{< /mermaid >}}