import json
from awsiot_credentialhelper.boto3_session import Boto3SessionProvider
import os

def create_boto3_session(endpoint, role_alias, certificate, private_key, thing_name, ca_cert_file):
    # Ensure CA certificate is read as bytes
    with open(ca_cert_file, 'rb') as ca_file:
        ca_cert_content = ca_file.read()
        if not isinstance(ca_cert_content, bytes):
            raise ValueError("CA certificate content must be bytes")

    # Ensure the certificate and private key are read as bytes (optional if needed for verification)
    with open(certificate, 'r') as cert_file:
        cert_content = cert_file.read()
        if not isinstance(cert_content, str):
            raise ValueError("Certificate content must be a string")

    with open(private_key, 'r') as key_file:
        key_content = key_file.read()
        if not isinstance(key_content, str):
            raise ValueError("Private key content must be a string")

    # Create boto3 session object
    boto3_session = Boto3SessionProvider(
        endpoint=endpoint,
        role_alias=role_alias,
        certificate=certificate,
        private_key=private_key,
        thing_name=thing_name,
    ).get_session()

    return boto3_session

# Replace these placeholders with your actual values
endpoint = "credential endpoint"
#find "aws iot describe-endpoint --endpoint-type iot\:CredentialProvider --output text"
role_alias = "IoT role alias"
certificate = "cert.pem file"
private_key = "private.key file"
thing_name = "things name"
ca_cert_file = "root-CA.crt"
#curl --silent 'https://www.amazontrust.com/repository/SFSRootCAG2.pem'   --output ./root-CA.crt
try:
    boto3_session = create_boto3_session(endpoint, role_alias, certificate, private_key, thing_name, ca_cert_file)
    BUCKET_NAME="bucket name"
    OBJECT_PATH="objectpath"
    OBJECT_KEY="object key in bucket"
    

    # Use the session to get the caller identity
    caller_identity = boto3_session.client("sts").get_caller_identity()
    print(caller_identity)
    s3_client = boto3_session.client('s3')
    objects=s3_client.upload_file(OBJECT_PATH, BUCKET_NAME, OBJECT_KEY)
except Exception as e:
    print(f"Error: {e}")
