import boto3

ec2Client = boto3.client('ec2')
ec2Resource = boto3.resource('ec2')

# Lambda function that associates AWS Elastic IP to tagged instances
# Triggered by CloudWatch Events -> when an instance state changes to Running
# It will only associate the Elastic IP to the tagged instance
def lambda_handler(event, context):
    # Elastic IP Allocation ID
    allocationID = '<Put here the elastic IP allocation id>'
    # Filter the instance by Tag
    instanceByTag = ec2Resource.instances.filter(
        Filters=[
            {
                'Name': 'tag:<Put here the Tag Key>',
                'Values': [
                    '<Put here the Value>'
                ]
            }
        ]
    )
    # Instance ID
    for instance in instanceByTag:
        instanceID = instance.id
    # Associating the Elastic IP to the tagged instance   
    associateEip = ec2Client.associate_address(
        InstanceId =  instanceID,
        AllocationId = allocationID
    )
