import boto3
import urllib.parse
import cv2
import numpy as np
from io import BytesIO
import logging
import sys

# Initialize the S3 clients
s3_client = boto3.client('s3')

def lambda_handler(event, context):
    # Initialize Logging
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler(sys.stdout)
    logger.addHandler(stream_handler)

    # Extract object key and object url from stepfunction payload
    object_key = event['object_key']
    object_url = event['object_url']
    bucket_name = event['bucket']
    
    logger.info(object_key)
    logger.info(object_url)
    
    # Extract "image_id" from object key
    key_parts = object_key.split('/')
    image_id_with_extension = key_parts[-1]
    image_id = '.'.join(image_id_with_extension.split('.')[:-1])  # Remove the file extension

    # Preprocess image
    
    # Download image from S3
    file_obj = s3_client.get_object(Bucket=bucket_name, Key=object_key)
    image_file_body = file_obj['Body'].read()
    
    # Decode image
    image_array = np.frombuffer(image_file_body, dtype=np.uint8)
    orig_image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    logger.info('cleared')
    
    return {
        'statusCode': 200,
        'body': f"Successfully processed {object_key}."
    }
