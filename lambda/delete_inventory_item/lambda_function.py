import boto3
import json

def lambda_handler(event, context):
    # Initialize DynamoDB client
    dynamo_client = boto3.client('dynamodb')
    table_name = 'InventoryApp'

    # Extract 'id' and 'location_id' from the path parameters
    if 'pathParameters' not in event or 'id' not in event['pathParameters'] or 'location_id' not in event['pathParameters']:
        return {
            'statusCode': 400,
            'body': json.dumps("Missing 'id' or 'location_id' path parameter")
        }

    item_id = event['pathParameters']['id']
    item_location_id = int(event['pathParameters']['location_id'])  # Convert to integer as it's a Number in the schema

    # Prepare the key for DynamoDB (partition key and sort key)
    key = {
        'item_id': {'S': item_id},  # Partition key
        'item_location_id': {'N': str(item_location_id)}  # Sort key (must be passed as string)
    }

    # Attempt to delete the item from the table
    try:
        dynamo_client.delete_item(TableName=table_name, Key=key)
        return {
            'statusCode': 200,
            'body': json.dumps(f"Item with ID {item_id} and Location ID {item_location_id} deleted successfully.")
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error deleting item: {str(e)}")
        }
