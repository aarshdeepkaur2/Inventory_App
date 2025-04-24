import boto3
import json

def lambda_handler(event, context):
    # DynamoDB setup
    dynamo_client = boto3.client('dynamodb')
    table_name = 'InventoryApp'

    # Log the event to inspect its structure
    print("Received event:", event)

    # Get the key parameters from the path parameters
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

    # Get the item from the table
    try:
        response = dynamo_client.get_item(TableName=table_name, Key=key)
        item = response.get('Item', {})

        if not item:
            return {
                'statusCode': 404,
                'body': json.dumps('Item not found')
            }

        # Convert DynamoDB types to standard Python types
        def deserialize(d):
            return {
                k: float(v['N']) if 'N' in v else v.get('S', '') for k, v in d.items()
            }

        cleaned_item = deserialize(item)

        return {
            'statusCode': 200,
            'body': json.dumps(cleaned_item, default=str)  # Use str to handle any special types like Decimal
        }

    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }
