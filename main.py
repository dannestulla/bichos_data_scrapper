import json
import os
import subprocess
import boto3
from botocore.config import Config
from credentials import bucket_name, r2_endpoint, access_key, secret_key
from botocore.exceptions import NoCredentialsError

from downloaded_files_csv import read_csv_file, write_files_downloaded_to_csv

pages = [
    #CANOAS
    "acheseudogulbra",
    "acheseupetrs",
    "animaisresgatadosmathias",
    "caesresgatadoscanoas",
    "dogs_da_acucena",
    "meubichotasalvocanoas",
    'onlycats.canoas',
    "petresgatado_canoas",
    "resgatadoagoracanoas",
    "resgatados.pasqualini",
    "resgatadosnazario409",
    "tosalvo.pet",

    #PORTO ALEGRE
    "acheseupetpoa",
    "adotareencontrarpets",
    "animais_resgatados_enchentepoa",
    "animaisresgatadosarandi",
    "pets_resgatadospoa",
    "petsperdidospoa",
    "pontalanimais",
    "resgatados.centrovida",
    "resgatados_ipa",
    "resgatadosdasilhas",
    "tosalvopetpoa",

    #SAO LEO
    "aumigos_enchentessl",
    "enchenters_dogs",
    "tosalvoanimaisrs",
]


def main():
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


def run_instaloader(pages):
    # fast-update just downloads new pics
    for page in pages:
        comando = 'instaloader --fast-update --no-videos --no-metadata --no-profile-pic --post-filter="date_utc >= datetime(2024, 5, 10)" ' + page
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


def create_folder_paths(pages):
    folderPaths = []
    for page in pages:
        folderPaths.append('C:\\Users\\dannn\\IdeaProjects\\BichosResgate\\bichos_data_scrapper\\' + page)
    return folderPaths


def get_files_paths(folder_path):
    images_paths = []
    for file in os.listdir(folder_path):
        if file.endswith(('.jpeg', '.jpg', '.png', '.gif', '.bmp', '.txt')):
            full_path = os.path.join(folder_path, file)
            images_paths.append(full_path)
    print(f"Caminho {folder_path} criado")
    return images_paths


def create_boto_client():
    return boto3.client('s3',
                        endpoint_url=r2_endpoint,
                        aws_access_key_id=access_key,
                        aws_secret_access_key=secret_key,
                        config=Config(signature_version='s3v4'),
                        region_name='auto'
                        )


def upload_to_s3(list_images, page, s3_client):
    for image_file_name in list_images:
        file_name = image_file_name.split('/')[-1]
        file_path2 = 'C:\\Users\\dannn\\IdeaProjects\\BichosResgate\\bichos_data_scrapper\\' + page + '\\' + file_name
        try:
            print("Uploading " + image_file_name)
            s3_client.upload_file(file_path2, bucket_name, image_file_name)
        except NoCredentialsError:
            print("Credenciais não disponíveis")
            return False


def check_if_folders_exist(folder_paths):
    for folder_path in folder_paths:
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)


def upload_file_list_to_s3(page, s3_client):
    file_list_location = "C:\\Users\\dannn\\IdeaProjects\\BichosResgate\\bichos_data_scrapper\\bichos_data_scrapper\\" + page + ".csv"
    s3_client.upload_file(file_list_location, bucket_name, page + ".csv")
    print(f"Enviada lista de arquivos baixados da pagina {page}")


if __name__ == "__main__":
    main()
