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
 
 
@app.route("/check")
def get_user():
    # resp = client.get_item(
    #     TableName=USERS_TABLE,
    #     Key={
    #         'userId': { 'S': user_id }
    #     }
    # )
    # item = resp.get('Item')
    # if not item:
    #     return jsonify({'error': 'User does not exist'}), 404
 
    # return jsonify({
    #     'userId': item.get('userId').get('S'),
    #     'name': item.get('name').get('S')
    # })
    return jsonify({
        'REQUESTS_TABLE': REQUESTS_TABLE,
        'SQS_QUEUE_URL': SQS_QUEUE_URL
    })
 
 
@app.route("/crawl", methods=["POST"])
def create_user():
    # user_id = request.json.get('userId')
    # name = request.json.get('name')
    # if not user_id or not name:
    #     return jsonify({'error': 'Please provide userId and name'}), 400
 
    # resp = client.put_item(
    #     TableName=USERS_TABLE,
    #     Item={
    #         'userId': {'S': user_id },
    #         'name': {'S': name }
    #     }
    # )
    response = sqs.send_message(
        QueueUrl=SQS_QUEUE_URL,
        DelaySeconds=10,
        MessageAttributes={
            'Title': {
                'DataType': 'String',
                'StringValue': 'The Whistler'
            },
            'Author': {
                'DataType': 'String',
                'StringValue': 'John Grisham'
            },
            'WeeksOn': {
                'DataType': 'Number',
                'StringValue': '6'
            }
        },
        MessageBody=(
            'Information about current NY Times fiction bestseller for '
            'week of 12/11/2016.'
        )
    )

    print(response['MessageId'])
    return jsonify({
        'messageId': response['MessageId']
    })