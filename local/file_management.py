import os

from model.credentials import folder_path


def get_folder_paths(pages):
    folderPaths = []
    for page in pages:
        folderPaths.append(folder_path + 'database\\' + page)
    return folderPaths


def get_files_path(folder_path):
    images_paths = []
    for file in os.listdir(folder_path):
        if file.endswith(('.jpeg', '.jpg', '.png', '.gif', '.bmp', '.txt')):
            full_path = os.path.join(folder_path, file)
            images_paths.append(full_path)
    print(f"Path {folder_path} created")
    return images_paths


def check_if_folders_exist(folder_paths):
    for folder_path in folder_paths:
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
