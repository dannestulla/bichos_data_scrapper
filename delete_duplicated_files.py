import os

import difPy

from local.csv_management import write_files_to_csv
from local.file_management import get_files_path, get_folder_paths
from main_script import remove_file_full_path
from model.credentials import database_path
from model.pages_model import pages





if __name__ == "__main__":
    delete_duplicated_files()
