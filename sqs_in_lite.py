import json
import boto3

sqs = boto3.client('sqs')
queue_url = 'https://sqs.region.amazonaws.com/account-id/queue-name'

def lambda_handler(event, context):
    data = json.loads(event['body'])
    response = sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=json.dumps(data)
    )
    return {
        'statusCode': 200,
        'body': json.dumps('Data sent to SQS successfully')
    }
