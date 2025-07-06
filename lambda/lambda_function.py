import json
import boto3
import os
from datetime import datetime
import random
import re
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

def lambda_handler(event, context):
    logger.info(f"Lambda function invoked with event: {json.dumps(event, default=str)}")
    
    try:
        # Handle API Gateway v2 (HTTP API) event structure
        http_method = event.get('requestContext', {}).get('httpMethod', {})
        raw_path = event.get('resource', '')
        
        logger.info(f"HTTP Method: {http_method}, Path: {raw_path}")
        
        if http_method == 'POST' and raw_path == '/register':
            logger.info("Calling register_user function")
            return register_user(event)
        elif http_method == 'GET' and raw_path == '/users':
            logger.info("Calling get_users function")
            return get_users()
        else:
            logger.warning(f"Route not found - Method: {http_method}, Path: {raw_path}")
            return {
                'statusCode': 404,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'error': 'Not found',
                    'method': http_method,
                    'path': raw_path
                })
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': str(e),
                'event': json.dumps(event, default=str)
            })
        }

def register_user(event):
    logger.info("Starting user registration")
    try:
        body = json.loads(event['body'])
        logger.info(f"Request body: {body}")
        
        # Validate required fields
        required_fields = ['firstName', 'lastName', 'email', 'phoneNumber', 'addressLn1', 'city', 'state', 'country']
        for field in required_fields:
            if not body.get(field):
                return {
                    'statusCode': 400,
                    'headers': {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*'
                    },
                    'body': json.dumps({'error': f'{field} is required'})
                }
        
        # Basic validation
        if not validate_email(body['email']):
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'error': 'Invalid email format'})
            }
        
        if len(body['firstName']) > 25 or len(body['lastName']) > 25:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'error': 'Name fields must be 25 characters or less'})
            }
        
        # Generate 7-digit customer ID
        customer_id = random.randint(1000000, 9999999)
        
        # Create user record
        user_record = {
            'Customer_Id': customer_id,
            'First_Name': body['firstName'][:25],
            'Last_Name': body['lastName'][:25],
            'Email': body['email'][:50],
            'Phone_Number': body['phoneNumber'][:15],
            'Address_Ln_1': body['addressLn1'][:100],
            'City': body['city'][:20],
            'State': body['state'][:15],
            'Country': body['country'][:15],
            'Start_Date': datetime.now().isoformat()
        }
        
        # Save to DynamoDB
        table.put_item(Item=user_record)
        
        return {
            'statusCode': 201,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'message': 'User registered successfully',
                'customerId': customer_id
            })
        }
        
    except json.JSONDecodeError:
        return {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': 'Invalid JSON'})
        }

def get_users():
    logger.info("Getting all users")
    try:
        response = table.scan()
        users = response['Items']
        logger.info(f"Found {len(users)} users")
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(users, default=str)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': str(e)})
        }

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None