import json
import uuid
from decimal import Decimal
import boto3

def lambda_handler(event, context):
    # Logging raw input (for debugging purposes only, remove in production)
    print("Received event:", json.dumps(event))

    # Parse JSON safely 
    try:
        body = event.get('body', '')
        if not body:
            raise ValueError("Empty body")

        data = json.loads(body)
    except (json.JSONDecodeError, ValueError) as e:
        return {
            'statusCode': 400,
            'body': json.dumps({"error": f"Bad request. Invalid JSON. {str(e)}"})
        }

    # Setup DynamoDB and added my table
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('InventoryApp')

    # Generate unique ID
    item_id = str(uuid.uuid4())

    # Convert numerical fields to correct types
    try:
        item_data = {
            'item_id': item_id,
            'item_location_id': int(data['item_location_id']),
            'item_name': data['item_name'],
            'item_description': data['item_description'],
            'item_qty_on_hand': int(data['item_qty_on_hand']),
            'item_price': Decimal(str(data['item_price']))  # safely convert to Decimal
        }
    except KeyError as e:
        return {
            'statusCode': 400,
            'body': json.dumps({"error": f"Missing required field: {str(e)}"})
        }
    except ValueError as e:
        return {
            'statusCode': 400,
            'body': json.dumps({"error": f"Invalid data format: {str(e)}"})
        }

    # Insert item into DynamoDB
    try:
        table.put_item(Item=item_data)
        return {
            'statusCode': 200,
            'body': json.dumps({"message": f"Item with ID {item_id} added successfully."})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({"error": f"Error adding item: {str(e)}"})
        }


