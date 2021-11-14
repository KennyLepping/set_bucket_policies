Some notes:

The aws cli has to be logged in to an IAM user with privileges
to modify S3 Buckets with boto3. To log in and out, one may have to delete
all folders from C:\Users\kenny\.aws

And then log in again with aws configure

https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html


{
        'Version': '2012-10-17',
        'Statement': [{
            'Sid': 'AddPerm',
            'Effect': 'Allow',
            'Principal': '*',
            'Action': ['s3:GetObject'],
            'Resource': f'arn:aws:s3:::{bucket_name}/*'
        }]
    }


How to run this project:
pip install Pipenv

pipenv shell

pip install -r requirements.txt

py main.py

Updating seems to be possible with this package:
https://stackoverflow.com/questions/34898335/amazon-s3-modify-bucket-policy-using-boto-boto3

TODO: Update policy instead create a new one


Update Everything but append Condition:

Sid: ForceSSL
Effect: Deny
Principal: *
Action: s3:* - stays the same
Resource: "arn:aws:s3::BUCKETNAME/*",
"Condition": {
    "Bool": {
        "aws:SecureTransport": "false"
    }
}