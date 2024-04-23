import boto3
import urllib.parse
import cv2
import numpy as np
from io import BytesIO


# Initialize the S3 and DynamoDB clients
s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

# Specify your DynamoDB table name
table_name = 'yolov8_images'
table = dynamodb.Table(table_name)
print(table)

def lambda_handler(event, context):
    # Extract bucket name and object key from the event
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    object_key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    object_url = f"https://{bucket_name}.s3.amazonaws.com/{object_key}"
    
    print(object_key)
    print(object_url)
    
    # Extract "image_id" from object key
    key_parts = object_key.split('/')
    image_id_with_extension = key_parts[-1]
    image_id = '.'.join(image_id_with_extension.split('.')[:-1])  # Remove the file extension
    
    # Check if item exists
    response = table.get_item(
        Key={
            'image_id': image_id
        }
    )
    
    # # If item exists, update it, otherwise put a new item
    # try:
    #     # If item exists, update it, otherwise put a new item
    #     if 'Item' in response:
    #         raise Exception(f"An image with the specified image_id [[[{image_id}]]] already exists.")
    #     else:
    #         table.put_item(
    #         Item={
    #             'image_id': image_id,
    #             'rawimage_objectkey': object_url
    #             }
    #         )

    # except Exception as e:
    #     print(f"Error: {e}")

    # Preprocess image
    
    # Download image from S3
    file_obj = s3_client.get_object(Bucket=bucket_name, Key=object_key)
    image_file_body = file_obj['Body'].read()
    
    # Decode image
    image_array = np.frombuffer(image_file_body, dtype=np.uint8)
    orig_image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    print('cleared')
    
    return {
        'statusCode': 200,
        'body': f"Successfully processed {object_key}."
    }
