import boto3

#The following script checks for unsused key pairs on AWS account
region = '<Region>'
ec2_client = boto3.client('ec2')
response = ec2_client.describe_key_pairs()['KeyPairs']
for key in response:
    found_instance = ec2_client.describe_instances(
        Filters=[
            {
                'Name': 'key-name',
                'Values': [key['KeyName']]
            }
        ]
    )['Reservations']
    if len(found_instance) == 0:
        print (key['KeyName'] + " is unused")