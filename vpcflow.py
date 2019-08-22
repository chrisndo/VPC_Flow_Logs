#!usr/bin/python
# python openAMLogin.py --username cndo --iamGroup FullAdmin
# arn:aws:s3:::fcs-vpcflowlogs-test

import boto3
import sys
import argparse
from pprint import pprint
from botocore.exceptions import ClientError
from botocore.exceptions import ProfileNotFound

#----------------------------------------------------------------------------
# get the command line arguments
#----------------------------------------------------------------------------

class init_args(object):

    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument(
            "--accountsfile", type=str, help="File containing AWS account alias names, one per line. " +
            "This configuration is required.", required=True)
        self.parser.add_argument(
            "--task", type=str, help="The task to perform. " +
            "This configuration is required.", required=True, 
            choices=['create', 'delete'])
        self.parser.add_argument(
            "--s3arn", type=str, help="The destination of the Flow Logs, which is an S3 ARN " +
            "This configuration ies required.", required=True)

        self.args = self.parser.parse_args(sys.argv[1:])

    def get_args(self):
        return self.args

def get_all_vpcs(ec2):
    return [vpc.id for vpc in list(ec2.vpcs.all())]

def enable_flow_logs(client, vpc_id, s3_arn):
    response = ''
    try:
        print("Trying to enable flow logs for:" + vpc_id)
        response = client.create_flow_logs(
            ResourceIds=[vpc_id],
            ResourceType="VPC",
            TrafficType="ALL",
            LogDestinationType="s3",
            LogDestination=s3_arn
        )
	if 'Unsuccessful' in response:
		if response['Unsuccessful']:
			if 'Message' in response['Unsuccessful'][0]['Error']:
				print("You might need to add this account to the S3 ARN Bucket Policy. \n" + 
				      response['Unsuccessful'][0]['Error']['Message'])
			else:
				print("Error creating flow log: ")
				print(str(response))
		else:
			print("Flow logs is successfully enabled for: " + vpc_id)
		
    except ClientError as e:
        if e.response['Error']['Code'] == "FlowLogAlreadyExists":
		print("Flow logs is already enabled for: " + vpc_id)
	elif e.response['Error']['Code'] == 'InvalidParameterValue':
		print("Invalid ARN parameter: " + s3_arn)
	else:
		print("Error: " + str(e))


def delete_flow_logs(client, flowid):
    try:
		response = client.delete_flow_logs(
			FlowLogIds = ['{}'.format(flowid)]
		)
	
    except ClientError as e:
        print("Error deleting flowlog ID: " + flowid + "\n" + str(e))
    else:
        print("Flow logs is successfully deleted for: " + flowid)

#----------------------------------------------------------------------------
# main 
#----------------------------------------------------------------------------

if __name__ == "__main__":
    args = init_args().get_args()
    
    account_aliases_input_file = args.accountsfile
    s3arn = args.s3arn
    task = args.task
    accounts_alias_list = []
    f = open(account_aliases_input_file, "r")

    for x in f:
        accounts_alias_list.append(x.rstrip())
    
    print("Will process these AWS account aliases:")
    pprint(accounts_alias_list)
	
    for account_alias in accounts_alias_list:
	session = None
		
	try:
		print('Trying account: ' + account_alias)
		session = boto3.Session(profile_name=account_alias)
        except ProfileNotFound as e:
		print('Account not found: ' + account_alias)
           	#print('Error: ' + str(e) + "\n")
            	continue
	
	try:
		resource = session.resource('ec2')
		client = session.client('ec2')
		vpcs =  [vpc.id for vpc in list(resource.vpcs.all())]
		
		if task == 'delete':
			dfb = client.describe_flow_logs()
			for i in range(len(dfb['FlowLogs'])):
				if dfb['FlowLogs'][i]['LogDestinationType'] == 's3': 
					if dfb['FlowLogs'][i]['LogDestination'] == s3arn:
						flowid = dfb['FlowLogs'][i]['FlowLogId']
						delete_flow_logs(client, flowid)
		
		if task == 'create':
			for vpc in vpcs:
				enable_flow_logs(client, vpc, s3arn)

	except ClientError as e:
		if e.response['Error']['Code'] == "RequestExpired":
			print('It looks like your access keys are not working, please get new ones.\n')
		else:
			print('Error found: ' + str(e.response))
	
