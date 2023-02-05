# Will Contain both the client for glacier and connection to it.
import boto3
from config import my_session, glacier_conf
from botocore.exceptions import ClientError
import os

glacier_client = my_session.client('glacier')

class VaultWrapper:
    """ Does basic Upload and Read functionality for particular Vault """
    def __init__(self,client,vaultName,returnBucket):
        """ The Vault name and the Glacier Connection from above """
        self.client = client # an glacier client
        self.vaultName = vaultName # the specific vault to be used
        self.returnBucket = returnBucket # the s3 Bucket where retrieval jobs are sent
    
    def upload_archive(self,archiveDescription,filePath):
        """ Uploads a single file """
        data = open(filePath,'rb')
        try:
            new_archive = self.client.upload_archive(vaultName=self.vaultName,archiveDescription=archiveDescription,body=data)
            print("Upload %s. New Achrive Id: %s to %s" % (archiveDescription, new_archive['archiveId'], self.vaultName))
            return new_archive
        except ClientError:
            print("Failed to complete upload to {self.vaultName}")
            print(ClientError)
            raise

    def describe_vault(self):
        """ Returns the vault details. """
        archives =  self.client.describe_vault(vaultName=self.vaultName)
        print(archives)
        return archives

    def get_archive(self,archiveId,description):
        """ Starts a job to put an Archive into a bucket """
        job_params = {
            'ArchiveId': archiveId,
            'Description': description,
            'Type': 'archive-retrieval',
            'OutputLocation': {
                'BucketName': returnBucket,
            }
        }
        job = self.client.initiate_job(
            vaultName = self.vaultName,
            jobParameters=job_params
        )
        print(job)
        return job
    
    def list_jobs(self,status='InProgress'):
        if status not in ['InProgress','Succeeded','Failed']:
            raise Exception("Status must be one of 'InProgress', 'Succeeded', or 'Failed'")
        else:
            jobs = self.client.list_jobs(
                vaultName=self.vaultName,
                statuscode = status
            )
            print(jobs)
            return jobs

    def get_inventory(self,startDate,endDate):
        """ Takes in dates in YYYY-MM-DD format and get the inventory for that time """
        formatStart = '%sT00:00:00Z' % (startDate)
        formateEnd = '%sT23:59:59Z' % (endDate)
        job_params = {
            'Type': 'inventory-retrieval',
            'Format': 'JSON',
            'InventoryRetrievalParameters': {
                'StartDate': formatStart,
                'EndDate': formateEnd,
            },
        }
        job = self.client.initiate_job(
            vaultName = self.vaultName,
            jobParameters=job_params
        )
        print(job)
        return job
