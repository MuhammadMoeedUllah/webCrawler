import hashlib
import os
import boto3
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone
client = boto3.client('dynamodb')
REQUESTS_TABLE = os.environ['REQUESTS_TABLE']


def getHash(string: str):
    return hashlib.sha256(string.encode()).hexdigest()

def insertToDB(messageId, title, url, contents, failedRecords):
	try:
		requestId = getHash(url)
		date = str(datetime.now().replace(tzinfo=timezone.utc))
		resp = client.put_item(
        TableName=REQUESTS_TABLE,
        Item={
            'requestId': {'S': requestId },
            'title': {'S': title },
			'date':{'S': date} ,
			'content': {'S':contents},
			'url': {'S': url}
			})
		print('Dynamo Response : ',resp)
	except Exception as e:
		print('error while inserting : ', requestId )
		print('exception : ', e)
		failedRecords.append(messageId)

def scrapURLElements (url): 
	try :
		reqs = requests.get(url)	
		soup = BeautifulSoup(reqs.text, 'html.parser')	
		titles = soup.find_all('title')
		if not titles or len(titles) < 1:
			titles = ''
		else:
			titles = titles[0].get_text()
		
		return titles, str(soup)
	except Exception as e:
		print('error while scraping : ', url )
		print('exception : ', e)
		return '', ''

def extractURL (record, failedRecords): 
	try :
		url = record['messageAttributes']['URL']['stringValue']
		return url
	except Exception as e:
		print('error while extracting url from record : ', record )
		print('exception : ', e)
		failedRecords.append(record['messageId'])
		return ''

def handler (event, context):
	failedRecords = []
	try :
		for record in event['Records']:
			url = extractURL(record, failedRecords)
			if len(url)>0:
				title, content = scrapURLElements(url)
				if title:
					insertToDB(record['messageId'],title,url,content,failedRecords)
				else:
					failedRecords.append(record['messageId'])
		print("failed records: ", failedRecords)	
		return failedRecords
	except Exception as e:
		print ('Exception : ', e)
		return ''

