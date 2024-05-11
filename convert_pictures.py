import os

def get_images_path():
    folder_path = 'C:\\Users\\dannn\\IdeaProjects\\BichosResgate\\bichos_data_scrapper\\meubichotasalvocanoas'
    images_path = []

    for file in os.listdir(folder_path):
        if file.endswith(('.jpeg', '.jpg', '.png', '.gif', '.bmp')):
            full_path = os.path.join(folder_path, file)
            images_path.append(full_path)

    return images_path

