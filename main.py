import json
import os
import subprocess
import boto3
from botocore.config import Config
from credentials import bucket_name, r2_endpoint, access_key, secret_key
from pictures_model import PostImages, post_pictures_serializer, Images
from botocore.exceptions import NoCredentialsError


def main():
    pages = ['meubichotasalvocanoas']
    #run_instaloader(pages)
    folder_path = 'C:\\Users\\dannn\\IdeaProjects\\BichosResgate\\bichos_data_scrapper\\' + pages[0]
    images_paths = get_images_path(pages, folder_path)
    upload_to_s3(images_paths, pages)


def run_instaloader(pages):
    # fast-update just downloads new pics
    comando = 'instaloader --fast-update --filename-pattern="{date_utc:%Y-%m-%d}" ' + pages[0]

    current_dir = os.getcwd()
    parent_dir = os.path.dirname(current_dir)
    run_instaloader_result = subprocess.run(comando, shell=True, text=True, cwd=parent_dir)

    if run_instaloader_result.returncode == 0:
        print("Comando executado com sucesso!")
    else:
        print("Erro ao executar comando!")


def get_images_path(pages, path):
    images_path = []
    for file in os.listdir(path):
        if file.endswith(('.jpeg', '.jpg', '.png', '.gif', '.bmp')):
            full_path = os.path.join(path, file)
            images_path.append(full_path)

    return images_path


def upload_to_s3(list_images, pages):
    count = 0
    s3_client = boto3.client('s3',
                             endpoint_url=r2_endpoint,
                             aws_access_key_id=access_key,
                             aws_secret_access_key=secret_key,
                             config=Config(signature_version='s3v4'),
                             region_name='auto'
                             )
    while count < 1:
        file_name = list_images[count].split('\\')[7]
        s3_file_name = pages[0] + '/' + file_name

        try:
            s3_client.upload_file(list_images[count], bucket_name, s3_file_name)
        except NoCredentialsError:
            print("Credenciais não disponíveis")
            return False
        count = count + 1
    prefix = '/gohan-bichos-resgate/'+pages[0]+'/'
    response = s3_client.list_objects_v2(Bucket='bichos-central', Prefix='gohan-bichos-resgate/')
    with open('files_names.txt', 'w') as files_names:
        files_names.write(response)
        s3_client.upload_file(files_names, 'bichos-central', 'files_names.txt')

if __name__ == "__main__":
    main()
