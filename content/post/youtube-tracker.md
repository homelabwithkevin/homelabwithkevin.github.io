+++
author = "Hugo Authors"
title = "YouTube Tracker"
date = "2023-04-21"
draft = true
description = "YouTube Tracker"
tags = [
    "youtube",
]
+++

As of August 2020, YouTube removed the feature for sending e-mail notifications for new content uploaded to channels you are subscribed to [[1]](https://support.google.com/youtube/thread/63269933?hl=en). I've relied on this system because sometimes I don't want to watch whatever is on the front page of YouTube.

While there are plenty of open-source alternatives, I wanted to try configure something myself.

#### Open-Source Alternatives
- https://github.com/yt-dlp/yt-dlp
- https://github.com/ytdl-org/youtube-dl
- https://github.com/Tzahi12345/YoutubeDL-Material
- https://gitlab.com/osp-group/flask-nginx-rtmp-manager
- https://github.com/tubearchivist/tubearchivist
- https://github.com/ViewTube/viewtube-vue

#### Tech Stack
- AWS Lambda for the backend API
- AWS API Gateway for the api to the Lambda function(s)
- AWS EC2 Spot Instances for the hosting
- AWS DynamoDB for the database
- AWS Simple Queue Service (SQS) for queuing
- AWS EventBrige for cron/scheduling tasks
- NextJS for the frontend website and a bit of middleware
- CloudFlare for DNS and CDN
- BackBlaze for video storage

#### Description
I started wth AWS Elastic Container Service on EC2 Spot, but the AMI that is configured is 30 GiB! So, I swithced to EC2 Spot Instance in an EC2 Auto Scaling Group. The EC2 instance has user-data which builds a docker image. There is an AWS Lambda Function that listens for auto-scaling events and updates the CloudFlare DNS record.

I wanted an easy way to save channels to DynamoDB. I have another Lambda and API Gateway which only allows my IP address. I rigged up a very basic Firefox extension to POST the channel URL and the Lambda takes care of the rest.

From there, I have an AWS Event Bridge that runs every 15 minutes which triggers a "List Channels" Lambda function. This functions all channels and for each channel publish to an AWS Simple Queue Service (SQS).

SQS then triggers and sends its payload to another function "Parse URL" which uses yt-dlp to get the most recent uploaded video and queries the database for the latest video. If both values are the same, do nothing. If the values are different, update the value in the database and publish to an AWS Simple Notification System (SNS) topic. 

The SNS topic sends to my email. I did have Google WorkSpace chat, which has webhook functionality. So, I did publish to that as well. I might integrate with RocketChat or Discord later, too. 

The frontend queries the database and has a similar layout as the actual YouTube page. So, I can click a thumbnail and it'll take me to the actual YouTube video. If I want to download the video, I can click a download button from my frontend. This downloads the video to BackBlaze. And CloudFlare is in front of that.

Pretty slick system. And mostly free, since it's all serverless.

#### Workflow for Saving Channels
1. Save YouTube Channel via Firefox extension
2. Triggers API Gateway which triggers "Save URL" Lambda Function
3. Updates "Channels" DynamoDB Table

#### Workflow for Getting New Uploads
1. Every 15-minutes, EventBridge triggers "List Channels" Lambda Function
2. Queries "Channels" DynamoDB Table and submits to SQS Queue
3. SQS Queue triggers "Parse URL" Lambda Function
4. Function gets channel's video from "Videos" table and downloads channel's information with yt-dlp
5. Function compares each value
6. If values are different (two different video ids), update the "Videos" table with the video id and publish to SNS Topic
7. SNS Topic sends email to me and publishes to webhook 

Sources
1. https://support.google.com/youtube/thread/63269933?hl=en