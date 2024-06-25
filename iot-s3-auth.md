1. ```aws cloudformation deploy  --template-file ./iot.yml --stack-name s3-auth-iot --capabilities CAPABILITY_IAM```

2. Role Alias

```aws iot create-role-alias   --role-alias S3DeviceIoTRoleAlias   --role-arn $(aws cloudformation describe-stacks \
    --output text \
    --stack-name s3-auth-iot \
    --query 'Stacks[0].Outputs[?OutputKey==`IAMRoleArn`].OutputValue')   --credential-duration-seconds 3600```
3. THING GROUP
THING_NAME=s3-auth-iot
THING_GROUP_NAME=s3IoTDevices

```THING_GROUP_ARN=$(aws iot create-thing-group \
  --output text \
  --thing-group-name $THING_GROUP_NAME \
  --query 'thingGroupArn')```


4. Create a thing

```aws iot create-thing \
  --thing-name "${THING_NAME}"

aws iot add-thing-to-thing-group \
  --thing-group-name $THING_GROUP_NAME \
  --thing-name $THING_NAME
```

5. Attach the policy

```aws iot attach-policy \
  --policy-name $(aws cloudformation describe-stacks \
    --output text \
    --stack-name s3-auth-iot \
    --query 'Stacks[0].Outputs[?OutputKey==`s3DevicePolicy`].OutputValue') \
  --target $THING_GROUP_ARN
```

6. Create Certificate

```
CERTIFICATE_ARN=$(aws iot create-keys-and-certificate --set-as-active \
  --certificate-pem-outfile ./device.cert.pem \
  --public-key-outfile ./device.public.key \
  --private-key-outfile ./device.private.key \
  --output text \
  --query 'certificateArn')
```

```
curl --silent 'https://www.amazontrust.com/repository/SFSRootCAG2.pem' \
  --output ./root-CA.crt
```
7. Attach Cert
```aws iot attach-thing-principal \
  --thing-name $THING_NAME \
  --principal $CERTIFICATE_ARN
```
8. Find all required credentials

endpoint = "credential endpoint"
#find "aws iot describe-endpoint --endpoint-type iot\:CredentialProvider --output text"
role_alias = "IoT role alias"
certificate = "cert.pem file"
private_key = "private.key file"
thing_name = "things name"
ca_cert_file = "root-CA.crt"



