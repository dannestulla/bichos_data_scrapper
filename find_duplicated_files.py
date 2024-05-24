import os
import subprocess
import difPy

from model.credentials import folder_path


def find_duplicated_files():
    # sub_folders = list_subfolder_names(folder_path+'database')
    # for folder in sub_folders:
    #     print(f"Analizando pasta {folder}")
    dif = difPy.build(folder_path + 'database', in_folder=True)
    search = difPy.search(dif)
    search.delete(silent_del=True)

# Função para listar nomes das subpastas
def list_subfolder_names(directory):
    subfolder_names = [f for f in os.listdir(directory) if os.path.isdir(os.path.join(directory, f))]
    return subfolder_names



if __name__ == "__main__":
    find_duplicated_files()
