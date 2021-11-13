Some notes:

The aws cli has to be logged in to an IAM user with privileges
to modify S3 Buckets with boto3. To log in and out, one may have to delete
all folders from C:\Users\kenny\.aws

And then log in again with aws configure




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

