import boto3
import json


def print_buckets():
    s3 = boto3.resource('s3')
    for bucket in s3.buckets.all():
        print(bucket.name)


def retrieve_bucket_policies(bucket: str):
    s3 = boto3.client('s3')
    result = s3.get_bucket_policy(Bucket=bucket)
    print(result['Policy'])


def set_bucket_policy(bucket: str):
    bucket_name = bucket
    bucket_policy = {
        "Version": "2012-10-17",
        "Statement": [{
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": {"AWS": "*"},
            "Action": "s3:*",
            "Resource":
                [
                    f"arn:aws:s3:::{bucket_name}",
                    f"arn:aws:s3:::{bucket_name}/*"
                ]
        }]
    }

    # Convert the policy from JSON dict to string
    bucket_policy = json.dumps(bucket_policy)

    # Set the new policy
    s3 = boto3.client('s3')
    s3.put_bucket_policy(Bucket=bucket_name, Policy=bucket_policy)


# AWS Account IDs: https://docs.aws.amazon.com/general/latest/gr/acct-identifiers.html
def change_valid_bucket_policies():
    s3 = boto3.resource('s3')
    s3_delete = boto3.client('s3')
    for bucket in s3.buckets.all():
        bucket_name = str(bucket.name)
        numbers_counter = 0
        for index in range(len(bucket_name)):
            if bucket_name[index].isdigit():
                numbers_counter += 1
            else:
                break

        if numbers_counter >= 6:
            set_bucket_policy(bucket.name)
            # s3_delete.delete_bucket_policy(Bucket=bucket.name)
            print(f"{bucket_name}'s policy has been changed to your new policy.")
