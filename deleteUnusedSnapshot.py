import boto3
from datetime import datetime, timedelta, timezone

#The following script delets unused snapshots and sends SNS notification
# def lambda_handler(event, context):
sns_client = boto3.client('sns')
ec2_client = boto3.client('ec2')
ec2_resource = boto3.resource('ec2')
snapshotIdsToDelete = []
# Create a list of snapshots by tag
snapshotsByTag = ec2_resource.snapshots.filter(Filters=[{
            'Name': 'tag:Name',
            'Values': [
                '<Value>',]},])
# 
for snapshot in snapshotsByTag:
    start_time = snapshot.start_time
    delete_time = datetime.now(tz=timezone.utc) - timedelta(days=1)
    if delete_time > start_time:
        snapshotIdsToDelete.append(snapshot.id)
# Pull all AMIs owned by the account
amisResponse = ec2_client.describe_images(Owners=['self'])
# Get list of all the snapshots associated with AMIs
for imageInfo in amisResponse['Images']:
    if 'Ebs' in amisResponse['Images'][0]['BlockDeviceMappings'][0]:
        snapshotId = (amisResponse['Images'][0]['BlockDeviceMappings'][0]['Ebs']['SnapshotId'])
        if snapshotId in snapshotIdsToDelete:
            # Remove all the snapshots that are associated with AMIs from the snapshotsByTag list
            snapshotIdsToDelete.remove(snapshotId)
            # Delete snapshot
            ec2_client.delete_snapshot(SnapshotId=snapshotId)
    
# Sending a message via SNS topic            
sns_client.publish(
TopicArn = '<topic-arn>',
Subject= 'Deleted snapshot list - <tag>',
Message = str(snapshotIdsToDelete)
)