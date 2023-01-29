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
        file = open(filePath,'rb')
        try:
            new_achrive = self.client.upload_archive(self.vaultName,archiveDescription,file)
            print("Upload %s. New Achrive Id: %s to {self.vaultName}" % (archiveDescription, new_achrive.id))
        except ClientError:
            print("Failed to complete upload to {slef.vaultName}")
            print(ClientError)
            raise
        else:
            return new_achrive
