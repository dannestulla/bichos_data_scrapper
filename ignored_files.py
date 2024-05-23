import os

import boto3
import pandas as pd
from botocore.config import Config
from datetime import datetime

from credentials import r2_endpoint, access_key, secret_key, bucket_name


def ignored_files():
    file_list_location = "C:\\Users\\dannn\\IdeaProjects\\BichosResgate\\bichos_data_scrapper\\" + "ignored_files" + ".csv"

    s3_client = boto3.client('s3',
                 endpoint_url=r2_endpoint,
                 aws_access_key_id=access_key,
                 aws_secret_access_key=secret_key,
                 config=Config(signature_version='s3v4'),
                 region_name='auto'
                 )
    s3_client.upload_file(file_list_location, bucket_name, "ignored_files" + ".csv")


if __name__ == "__main__":
    ignored_files()
