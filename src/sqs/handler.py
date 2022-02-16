import os
import boto3
client = boto3.client('dynamodb')
REQUESTS_TABLE = os.environ['REQUESTS_TABLE']

def handler (event, context):
	resp = client.put_item(
        TableName=REQUESTS_TABLE,
        Item={
            'requestId': {'S': 'asdasdasdasdasd' },
            'title': {'S': REQUESTS_TABLE },
			'data':{'S':'asdasdasdad'} })
	print('resp" ', resp)
	return
