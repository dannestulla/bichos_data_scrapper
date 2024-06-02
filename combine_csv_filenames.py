import csv
import os

import boto3
import pandas as pd
from botocore.config import Config
from datetime import datetime

from model.credentials import r2_endpoint, access_key, secret_key, bucket_name, folder_path


def combine_and_upload_file_list():
    """
    Combines all pages contents that are in .csv files into a single .csv.
    Then sorts the by date and sends to be consumed by frontend
    """

    current_directory = folder_path + 'folders_content_csv'

    combined_data = get_all_data_from_files(current_directory)

    combined_data = remove_ignored_files(combined_data)

    files_with_dates = set_files_dates(combined_data)

    output_filename = "combined_pages_data.csv"
    file_list_location = folder_path + output_filename

    try:
        os.remove(file_list_location)
    except OSError:
        print(f"Arquivo {file_list_location} nao encontrado")

    sorted_files = [file[0] for file in files_with_dates]

    pd.DataFrame(sorted_files).to_csv(output_filename, index=False, header=False)

    print(f"All csv files where combined in em {output_filename}")



    s3_client = boto3.client('s3',
                             endpoint_url=r2_endpoint,
                             aws_access_key_id=access_key,
                             aws_secret_access_key=secret_key,
                             config=Config(signature_version='s3v4'),
                             region_name='auto'
                             )
    s3_client.upload_file(file_list_location, bucket_name, "combined_pages_data" + ".csv")
    print("combined_pages_data.csv uploaded")


def get_all_data_from_files(directory):
    all_data = []
    for filename in os.listdir(directory):
        try:
            if filename.endswith(".csv"):
                # Ler o arquivo CSV
                filepath = os.path.join(directory, filename)
                df = pd.read_csv(filepath, header=None)

                # Adicionar o DataFrame à lista
                all_data.append(df)
        except Exception as e:
            print(e)
    return pd.concat(all_data, ignore_index=True).values.tolist()


def set_files_dates(data):
    files_with_dates = []
    for file in data:
        try:
            date_str = file[0].split('/')[1].split('_UTC')[0]
            date_str = date_str.replace('_', ' ')

            # Converter a data para o formato DateTime
            file_date = datetime.strptime(date_str, "%Y-%m-%d %H-%M-%S")

            # Adicionar o arquivo e a data à lista
            files_with_dates.append((file, file_date))
        except Exception as e:
            print(e)

    files_with_dates.sort(key=lambda x: x[1], reverse=True)
    return files_with_dates


def remove_ignored_files(files):
    ignored_files = read_ignored_files_csv()
    files_to_remove = [file for file in files if any(ignored in file for ignored in ignored_files)]

    for file in files_to_remove:
        files.remove(file)
        print(f"Ignoring file {file}")

    return files


def contains_substring(lista, substring):
    return any(substring in elemento for elemento in lista)


def read_ignored_files_csv():
    ignored_files_path = folder_path + "ignored_files" + ".csv"
    files_list = []
    try:
        with open(ignored_files_path, 'r', newline='') as csv_file:
            csv_reader = csv.reader(csv_file)
            for line in csv_reader:
                files_list.append(line[0])
    except FileNotFoundError:
        print()
    return files_list


if __name__ == "__main__":
    combine_and_upload_file_list()
