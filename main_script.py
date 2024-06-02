import os
import subprocess
import boto3
import difPy
from botocore.config import Config

from combine_csv_filenames import combine_and_upload_file_list
from model.credentials import r2_endpoint, access_key, secret_key, database_path, csv_files, insta_pass
from datetime import date
from local.csv_management import read_csv_file, write_files_to_csv
from local.file_management import get_files_path, get_folder_paths, check_if_folders_exist
from model.pages_model import pages
from remote.upload_data import upload_files


def main_script():
    run_instaloader(pages)
    folder_paths = get_folder_paths(pages)
    check_if_folders_exist(folder_paths)
    s3_client = create_boto_client()
    index = 0
    for page in pages:
        files_paths = get_files_path(folder_paths[index])
        files_already_downloaded = read_csv_file(csv_files + page + ".csv")
        files_just_downloaded = remove_file_full_path(files_paths)
        new_files = [item for item in files_just_downloaded if item not in files_already_downloaded]
        upload_files(new_files, page, s3_client)
        write_files_to_csv(files_just_downloaded, page)
        index += 1
    delete_duplicated_files()
    combine_and_upload_file_list()


def run_instaloader(pages):
    date_today = date.today()
    day = date_today.strftime("%d")
    #
    for page in pages:
        comando = f'instaloader --no-videos --login=dannestulla --password={insta_pass} --no-metadata --no-profile-pic --fast-update ' + page
        run_instaloader_result = subprocess.run(comando, shell=True, text=True, cwd=database_path)
        if run_instaloader_result.returncode == 0:
            print("run_instaloader executado com sucesso!")
        else:
            print("Error when runing instaloader")


def remove_file_full_path(files_paths):
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


def delete_duplicated_files():
    dif = difPy.build(database_path, in_folder=True)
    search = difPy.search(dif, similarity='similar')
    print(f"Duplicate: {search.result}")
    search.delete(silent_del=True)

    folder_paths = get_folder_paths(pages)
    index = 0
    for page in pages:
        files_paths = get_files_path(folder_paths[index])
        files = remove_file_full_path(files_paths)
        write_files_to_csv(files, page)
        index += 1


if __name__ == "__main__":
    main_script()
