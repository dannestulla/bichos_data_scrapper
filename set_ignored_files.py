import boto3
from botocore.config import Config

from model.credentials import r2_endpoint, access_key, secret_key, bucket_name, folder_path


def set_ignored_files():
    """
    Creates a list of ignored files that are set manually using the client.
    This .csv is then sent to the client, so it will ignore files written in it
    """
    file_list_location = folder_path + "ignored_files" + ".csv"

    s3_client = boto3.client('s3',
                 endpoint_url=r2_endpoint,
                 aws_access_key_id=access_key,
                 aws_secret_access_key=secret_key,
                 config=Config(signature_version='s3v4'),
                 region_name='auto'
                 )
    s3_client.upload_file(file_list_location, bucket_name, "ignored_files" + ".csv")



if __name__ == "__main__":
    set_ignored_files()
