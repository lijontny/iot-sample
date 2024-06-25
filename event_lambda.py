import json

def lambda_handler(event, context):
    parameters = event["Parameters"]
    bucket_name = parameters["S3bucket"]
    key_name = parameters["S3key"]
    print(f"Bucket Name: {bucket_name}")
    print(f"Key Name: {key_name}")
    return {
        'statusCode': 200,
        'body': json.dumps(key_name)
    }