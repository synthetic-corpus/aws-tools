# Will Contain both the client for glacier and connection to it.
import boto3
from config import my_session, glacier_conf
from botocore.exceptions import ClientError
import os

glacier_client = my_session.client('glacier')

class VaultWrapper:
    """ Does basic Upload and Read functionality for particular Vault """
    def __init__(self,client,vaultName):
        """ The Vault name and the Glacier Connection from above """
        self.client = client
        self.vaultName = vaultName

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
