import json
import os
import subprocess
import boto3

import requests

from convert_pictures import get_images_path, prepare_image
from credentials import bucket_name
from pictures_model import PostImages, post_pictures_serializer, Images
from botocore.exceptions import NoCredentialsError

def main():
    # run_instaloader()
    images_paths = get_images_path()
    # prepared_image = prepare_image(images_paths)
    # treated_data = treat_data(prepared_image)
    upload_to_s3(images_paths)


def run_instaloader():
    # fast-update just downloads new pics
    comando = 'instaloader --fast-update profile meubichotasalvocanoas'

    current_dir = os.getcwd()
    parent_dir = os.path.dirname(current_dir)
    run_instaloader_result = subprocess.run(comando, shell=True, text=True, cwd=parent_dir)

    if run_instaloader_result.returncode == 0:
        print("Comando executado com sucesso!")
    else:
        print("Erro ao executar comando!")


def treat_data(images):
    images_list = []
    for image in images:
        images_list.append(Images(image))

    post_pictures = PostImages(page='meubichotasalvocanoas', images=images_list)
    json_data = json.dumps(post_pictures, default=post_pictures_serializer, indent=4)
    return json_data


def upload_to_s3(list_images):
    file_name = list_images[0].split('\\')[7]
    s3_file_name = 'meubichotasalvocanoas'+'\\'+file_name
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(list_images[0], bucket_name, s3_file_name)
    except NoCredentialsError:
        print("Credenciais não disponíveis")
        return False


if __name__ == "__main__":
    main()
