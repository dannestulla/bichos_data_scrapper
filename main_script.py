import os
import subprocess
import boto3
from botocore.config import Config

from find_duplicated_files import find_duplicated_files
from model.credentials import r2_endpoint, access_key, secret_key
from datetime import date
from local.csv_management import read_csv_file, write_files_downloaded_to_csv
from local.file_management import get_files_paths, create_folder_paths, check_if_folders_exist
from model.pages_model import pages
from remote.upload_data import upload_to_s3, upload_file_list_to_s3
from combine_csv_filenames import combine_csv_filenames


def main_script():
    run_instaloader(pages)
    folder_paths = create_folder_paths(pages)
    check_if_folders_exist(folder_paths)
    s3_client = create_boto_client()
    index = 0
    for page in pages:
        page_file_paths = get_files_paths(folder_paths[index])
        files_already_downloaded = read_csv_file(page, page_file_paths)
        files_just_downloaded = check_files_just_downloaded(page_file_paths)
        files_not_uploaded = [item for item in files_just_downloaded if item not in files_already_downloaded]
        upload_to_s3(files_not_uploaded, page, s3_client)
        write_files_downloaded_to_csv(files_not_uploaded, page)
        upload_file_list_to_s3(page, s3_client)
        index += 1
    find_duplicated_files()
    combine_csv_filenames()


def run_instaloader(pages):
    # fast-update just downloads new pics
    date_today = date.today()
    day = date_today.strftime("%d")
    for page in pages:
        comando = f'instaloader --latest-stamps --no-videos --no-metadata --no-profile-pic --post-filter="date_utc >= datetime(2024, 5, {day})" ' + page
        current_dir = os.getcwd()
        parent_dir = os.path.dirname(current_dir)
        run_instaloader_result = subprocess.run(comando, shell=True, text=True, cwd=parent_dir)
        if run_instaloader_result.returncode == 0:
            print("run_instaloader executado com sucesso!")
        else:
            print("Erro ao executar comando!")


def check_files_just_downloaded(files_paths):
    file_names = []
    for file_name in files_paths:
        file_names.append(file_name.split("\\")[-2] + "/" + file_name.split("\\")[-1])
    return file_names


def create_boto_client():
    return boto3.client('s3',
                        endpoint_url=r2_endpoint,
                        aws_access_key_id=access_key,
                        aws_secret_access_key=secret_key,
                        config=Config(signature_version='s3v4'),
                        region_name='auto'
                        )


if __name__ == "__main__":
    main_script()
