import utils.helpers as helper
import os
import boto3
from flask import Flask, jsonify, request
app = Flask(__name__)
 
REQUESTS_TABLE = os.environ['REQUESTS_TABLE']
SQS_QUEUE_URL = os.environ['SQS_QUEUE_URL']
client = boto3.client('dynamodb')
sqs = boto3.client('sqs')
 
@app.route("/")
def health():
    return "This stream is healthy!"
 
 
@app.route("/check/<string:identifier>")
def get_user(identifier):
    try:
        resp = client.get_item(
            TableName=REQUESTS_TABLE,
            Key={
                'requestId': { 'S': identifier }
            }
        )
        

        item = resp.get('Item')
        if not item:
            return helper.getErrResponse('No entry found for this identifier')
        data =  jsonify({
            'content' : item['content']['S'],
            'title' : item ['title']['S'],
            'date' : item ['date']['S'],
            'url' : item ['url']['S']
        })

        return helper.getSuccessResponse(data)
    except Exception as e:
        print('Exception : ', e)
        return helper.getErrResponse('oops!')
 
@app.route("/crawl", methods=["POST"])
def create_user():
    try:
        url = request.json['url']

        # check for parameters
        if not url :
            print("input params [URL] not valid")
            return helper.getErrResponse('Make sure to provide url in body as \{"url":"www.example.com" \}')
         
        # attempt enqueue data in to SQS
        response = sqs.send_message(
            QueueUrl=SQS_QUEUE_URL,
            DelaySeconds=0,
            MessageAttributes={
                'URL': {
                    'DataType': 'String',
                    'StringValue': url
                },
            },
            MessageBody=(
                'url for crawl '
            )
        )
        print('response: ', response)
        #check for errors whule enqueue
        if not response or not response['MessageId']:
            print('Something went wrong while enque')
            return helper.getErrResponse('Somethnig went wrong')
 
        identifier  = helper.getHash( response['MessageId'] + url)
        print('identifier : ', identifier)
        return helper.getSuccessResponse(jsonify({'identifier':identifier }))

    except Exception as e:
       print ("exception : ",e) 
       print ("Input : ", request.json)
       return helper.getErrResponse('Internal Server Error')
