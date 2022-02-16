# Web Crawler
![CircleCI](https://circleci.com/gh/MuhammadMoeedUllah/Object-Pool.svg?style=svg)

## Introduction

Web crawler is a simple application based on AWS cloud services.
This app uses `serverless` tool for deploying to the cloud.

## Dependencies

. serverless
    - Framework Core: 3.2.1
    - Plugin: 6.0.0
    - SDK: 4.3.1
. Python 3.6
. aws credentials

Python packages required for this project are list in the `requirements.txt` file in the core directory.

## Run the Project 

An already deployed version of this project is accessible through following steps:
1. Download and install postman
2. import a collection from [here](https://www.getpostman.com/collections/13a3548d112275302458)
3. Run the Post Request and provide a url of your choice in the message body
4. copy the `identifier` from response of step 3
5. append/paste the `identifier` at the end of `GET request` url for eg  baseurl/dev/check/`paste identifier here` 

Yay, we have a working model to test out the API. Note for every request a new identifier is returned even the url you provided was same.

## Deploy the Project (more action!)

The project is based on `serverless` framework. To deploy it first you need to setup your AWS account and clone it. 
After acount setup you will be provided with 
    a. AWS_ACCESS_KEY_ID
    b. AWS_SECRET_ACCESS_KEY

Use them to set your terminal env vars as follows:
    . export AWS_ACCESS_KEY_ID=`your access key id`
    . export AWS_SECRET_ACCESS_KEY=`your secret access key`

Now got the cloned directory and run

```
serverless project init

-n <name> the name of your project.
-b <bucket> the bucket of your project.
-p <awsProfile> an AWS profile that is defined in ~/.aws/credentials file.
-s <stage> the first stage for your new project.
-r <region> a lambda supported region for your project.
-c <BOOLEAN> Optional - Doesn't execute CloudFormation if true. Default is false.

```
These above arguments you can use as per your need. First deployment will take some time. 
Once deployed you will get a publically accessible URL that you can use to make requests.

### Good LUCK !!

PS: the build badge is setup for my other project. I set it up for this repo latrer. But it looks cool :) 