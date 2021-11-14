import boto3
import json
from awspolicy import BucketPolicy


def print_buckets():
    s3 = boto3.resource('s3')
    for bucket in s3.buckets.all():
        print(bucket.name)


def retrieve_bucket_policies(bucket: str):
    s3 = boto3.client('s3')
    result = s3.get_bucket_policy(Bucket=bucket)
    print(result['Policy'])


# def set_bucket_policy(bucket: str, new_bucket_policy):
def change_bucket_policy(bucket: str):
    s3_client = boto3.client('s3')
    bucket_name = bucket
    bucket_policy = BucketPolicy(serviceModule=s3_client, resourceIdentifer=bucket_name)

    if bucket_policy.content.get('Id') is not None:
        bucket_id = bucket_policy.content.get('Id')
    else:
        bucket_id = None

    bucket_version = bucket_policy.content.get('Version')
    new_dict_for_sid = bucket_policy.content.get('Statement')[0]

    # I have to get the bucket statement based on it's name
    statement_to_modify = bucket_policy.select_statement(new_dict_for_sid.get('Sid'))

    # Assign new values here and then save the statement
    statement_to_modify.Sid = "ForceSSL"
    statement_to_modify.Effect = "Deny"
    statement_to_modify.Principal = "*"
    statement_to_modify.Resource = f"arn:aws:s3:::{bucket_name}/*"
    statement_to_modify.save()

    with open('s3_condition.json') as json_file:
        s3_condition = json.load(json_file)

    new_bucket_policy = statement_to_modify.content

    new_bucket_policy.update(s3_condition)

    if bucket_id is not None:
        bucket_policy = {
            "Version": bucket_version,
            "Id": bucket_id,
            "Statement": [
                new_bucket_policy
            ]
        }
    else:
        bucket_policy = {
            "Version": bucket_version,
            "Statement": [
                new_bucket_policy
            ]
        }

    # Convert the policy from JSON dict to string
    bucket_policy = json.dumps(bucket_policy)

    # Set the new policy
    s3 = boto3.client('s3')
    s3.put_bucket_policy(Bucket=bucket_name, Policy=bucket_policy)


# AWS Account IDs: https://docs.aws.amazon.com/general/latest/gr/acct-identifiers.html
def change_valid_bucket_policies():
    s3 = boto3.resource('s3')
    s3_client = boto3.client('s3')
    for bucket in s3.buckets.all():
        bucket_name = str(bucket.name)
        numbers_counter = 0
        for index in range(len(bucket_name)):
            if bucket_name[index].isdigit():
                numbers_counter += 1
            else:
                break

        if numbers_counter >= 6:
            # set_bucket_policy(bucket.name)
            # s3_delete.delete_bucket_policy(Bucket=bucket.name)
            change_bucket_policy(bucket.name)

            print(f"{bucket_name}'s policy has been changed to your new policy.")


# USE WITH CATUTION! This function updates the bucket policy of all buckets in the account.
# This is also untested, but change_bucket_policy() does work on my simple bucket policies
def change_all_bucket_policies():
    s3 = boto3.resource('s3')
    s3_delete = boto3.client('s3')
    for bucket in s3.buckets.all():
        change_bucket_policy(bucket.name)
        print(f"{bucket.name}'s policy has been changed to your new policy.")
