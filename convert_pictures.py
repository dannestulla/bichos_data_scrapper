import base64
import os
from dataclasses import dataclass

from PIL import Image
import io


def get_images_path():
    folder_path = 'C:\\Users\\dannn\\IdeaProjects\\BichosResgate\\bichos_data_scrapper\\meubichotasalvocanoas'
    images_path = []

    for file in os.listdir(folder_path):
        if file.endswith(('.jpeg', '.jpg', '.png', '.gif', '.bmp')):
            full_path = os.path.join(folder_path, file)
            images_path.append(full_path)

    return images_path


def prepare_image(image_paths):
    images = []
    for image_path in image_paths:
        with open(image_path, 'rb') as file:
            # Criar o dicionário 'file' conforme necessário para a requisição multipart/form-data
            file_data = {'file': (file.name, file.read(), 'image/jpeg')}
            # Adicionar o dicionário file_data e quaisquer dados adicionais a uma lista
            images.append({'file_data': file_data, 'data': {'other_field': 'value'}})
    return images



@dataclass
class ImageToSend:
    file: dict = "",
    data: dict = {},
