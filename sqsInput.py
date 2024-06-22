import json
import boto3
import hashlib
import hmac
import os

sqs = boto3.client('sqs')

def verify_hmac_signature(event_body, received_signature, secret):
    computed_signature = 'sha256=' + hmac.new(
        secret.encode(),
        event_body.encode(),
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(computed_signature, received_signature)

def lambda_handler(event, context):
    try:
        # Shared secret key
        secret = os.environ['WEBHOOK_SECRET']
        
        # Get the signature from the request headers
        signature = event['headers'].get('X-Hub-Signature-256')
        if not signature:
            return {
                'statusCode': 400,
                'body': json.dumps('Missing signature')
            }

        # Verify the HMAC signature
        if not verify_hmac_signature(event['body'], signature, secret):
            return {
                'statusCode': 403,
                'body': json.dumps('Invalid signature')
            }

        # Process the valid request
        body = json.loads(event['body'])
        
        # Send message to SQS
        queue_url = os.environ['SQS_QUEUE_URL']
        response = sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=json.dumps(body)
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps('Webhook processed successfully')
        }
    
    except json.JSONDecodeError:
        return {
            'statusCode': 400,
            'body': json.dumps('Invalid JSON payload')
        }
    
    except boto3.exceptions.Boto3Error as e:
        print(f"Boto3 error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps('Failed to send message to SQS')
        }
    
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps('Internal server error')
        }
