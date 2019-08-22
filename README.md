# VPC Flow Logs Script
This script will create VPC Flow Logs directed to a specific S3 Bucket ARN.  It will create Flow Logs for every VPC listed in the accounts specified in the accounts text file.  This requires the bucket policy to be modified to include every account you are creating VPC Flow Logs for, or there will be errors.

## Installation

The application needs AWS CLI credentials to be available. The openAMLogin.py script, below, will give you temporary credentials so that you can run the application.

SSH into a jump box which has network access to FCS's GitHub and the AWS accounts desired. Create a temporary directory (i.e "mkdir iamusers"). cd to the directory. Follow these commands:

```
git clone -b master https://YOURSHORTNAMEHERE@github.helix.gsa.gov/HelixDevOps/BSPUtilites.git

python BSPUtilites/python/openAM/openAMLogin.py  --username YOURSHORTNAMEHERE --iamGroup FullAdmin 

cd BSPUtilites/python/ManageIAMAccessKeys/
```

## Arguments
Required arguments:

**--accountsfile** -- name of file containing AWS account aliases, one per line (Example: accts.txt)

**--task** -- the task create or delete VPC Flow Logs (options are "create" or "delete")

**--s3arn** -- the S3 Bucket ARN that the VPC Flow Logs will be directed to

## Usage
To create VPC Flow Logs directed to a S3 Bucket ARN and output to screen and to a log file

```python vpcflow.py --accountsfile accts.txt --task create --s3arn arn:aws:s3:::fcs-vpcflowlogs-test | tee log.txt```

To create VPC Flow Logs directed to a S3 Bucket ARN and output to screen and to a log file

```python vpcflow.py --accountsfile accts.txt --task delete --s3arn arn:aws:s3:::fcs-vpcflowlogs-test | tee log.txt```
