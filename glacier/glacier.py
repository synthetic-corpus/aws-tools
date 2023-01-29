# Will Contain both the client for glacier and connection to it.
import boto3
from config import my_session, glacier_conf

glacier_client = my_session.client('glacier')
#glacier_resource = my_session.resource('glacier')
out_put = glacier_client.describe_vault(vaultName=glacier_conf['vaultName'])
print(out_put)