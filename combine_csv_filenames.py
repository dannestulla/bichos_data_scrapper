import os

import boto3
import pandas as pd
from botocore.config import Config
from datetime import datetime

from model.credentials import r2_endpoint, access_key, secret_key, bucket_name, folder_path


def combine_csv_filenames():
    """
    Combines all pages contents that are in .csv files into a single .csv.
    Then sorts the by date and sends to be consumed by frontend
    """

    # Definir o diretório atual
    current_directory = folder_path+'folders_content_csv'

    # Inicializar uma lista para armazenar os DataFrames
    all_data = []

    # Iterar sobre todos os arquivos no diretório atual
    for filename in os.listdir(current_directory):
        try:
            if filename.endswith(".csv"):
                # Ler o arquivo CSV
                filepath = os.path.join(current_directory, filename)
                df = pd.read_csv(filepath, header=None)

                # Adicionar o DataFrame à lista
                all_data.append(df)
        except Exception as e:
            print(e)

    # Concatenar todos os DataFrames
    combined_data = pd.concat(all_data, ignore_index=True).values.tolist()
    files_with_dates = []

    for file in combined_data:
        date_str = file[0].split('/')[1].split('_UTC')[0]
        date_str = date_str.replace('_', ' ')

        # Converter a data para o formato DateTime
        file_date = datetime.strptime(date_str, "%Y-%m-%d %H-%M-%S")

        # Adicionar o arquivo e a data à lista
        files_with_dates.append((file, file_date))

    files_with_dates.sort(key=lambda x: x[1], reverse=True)

    # Definir o nome do arquivo de saída
    output_filename = "combined_pages_data.csv"

    # Salvar o DataFrame combinado em um novo arquivo CSV

    sorted_files = [file[0] for file in files_with_dates]
    pd.DataFrame(sorted_files).to_csv(output_filename, index=False, header=False)

    print(f"Todos os dados foram combinados em {output_filename}")

    file_list_location = folder_path + "combined_pages_data" + ".csv"

    s3_client = boto3.client('s3',
                 endpoint_url=r2_endpoint,
                 aws_access_key_id=access_key,
                 aws_secret_access_key=secret_key,
                 config=Config(signature_version='s3v4'),
                 region_name='auto'
                 )
    s3_client.upload_file(file_list_location, bucket_name, "combined_pages_data" + ".csv")


if __name__ == "__main__":
    combine_csv_filenames()
