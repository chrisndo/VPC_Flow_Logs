# VPC_Flow_Logs
This script will create VPC Flow Logs directed to a specific S3 Bucket ARN. It will create Flow Logs for every VPC listed in the accounts specified in the accounts text file. This requires the bucket policy to be modified to include every account you are creating VPC Flow Logs for, or there will be errors.
