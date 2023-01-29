## This file to be ignored.
import boto3
from botocore.config import Config

this_config = Config(
    region_name = '' # The AWS Region
    signature_version = 'v4' # Using this version?
    retries = {
        'max_attemps': 10,
        'mode': 'standard'
    }
)

session = boot3.Session(profile_name='') # Put the name of the ~/.aws profile to be used here