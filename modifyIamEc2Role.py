import boto3

#The following script modifies the EC2 role
ec2Resource = boto3.resource('ec2')
ec2Client = boto3.client('ec2')
iamResource = boto3.resource('iam')
iamClient = boto3.client('iam')
sns_client = boto3.client('sns')
modiefiedEc2Profiles = []
allInstanceProfiles = []

instanceProfiles = iamResource.instance_profiles.all()
for instanceProfile in instanceProfiles:
    allInstanceProfiles.append(instanceProfile.name)
for instance in ec2Resource.instances.all():
    intanceProfileInfo = ec2Client.describe_iam_instance_profile_associations(
        Filters=[
            {
                'Name': 'instance-id',
                'Values': [
                    instance.id,
                ]
            },
        ]
    )
    if intanceProfileInfo['IamInstanceProfileAssociations'] == []:
        instanceRoleAssociate = ec2Client.associate_iam_instance_profile(
            IamInstanceProfile={
                'Arn': '<RoleArn>',
                'Name': '<RoleName>'
            },
            InstanceId = instance.id
    )
    else:    
        iamInstaceProfileARN = intanceProfileInfo['IamInstanceProfileAssociations'][0]['IamInstanceProfile']['Arn']
        ec2InstanceProfileName = iamInstaceProfileARN.partition("/")[2]
        if ec2InstanceProfileName not in modiefiedEc2Profiles and ec2InstanceProfileName in allInstanceProfiles:
            modiefiedEc2Profiles.append(ec2InstanceProfileName)
            attachPolicy = iamClient.attach_role_policy(
                RoleName = ec2InstanceProfileName,
                PolicyArn = '<PolicyARN>'
            )

# Sending a message via SNS topic            
sns_client.publish(
TopicArn = '<topic-arn>',
Subject= 'Deleted snapshot list - <tag>',
Message = str()
)