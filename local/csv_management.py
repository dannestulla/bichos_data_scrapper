import csv
import os

from model.credentials import csv_files


def create_csv_file(file_name, files_list):
    with open(file_name, 'w', newline='') as csv_file:
        csv_writter = csv.writer(csv_file)
    print(f"{file_name}'.csv' created.")
    return files_list


def read_csv_file(file_path):
    files_list = []
    try:
        with open(file_path, 'r', newline='') as csv_file:
            csv_reader = csv.reader(csv_file)
            for line in csv_reader:
                files_list.append(line[0])

        print(f"Reading {file_path}")
        return files_list
    except FileNotFoundError:
        create_csv_file(file_path, files_list)
        return files_list


def write_files_to_csv(files_just_uploaded, page):
    file_path = csv_files + page + '.csv'
    current_file_data = read_csv_file(file_path)
    print(f"removing {file_path}")
    try:
        os.remove(file_path)
    except FileNotFoundError:
        print()
    with open(file_path, 'a', newline='') as csv_file:
        csv_writter = csv.writer(csv_file)
        for file in files_just_uploaded:
            csv_writter.writerow([file])
    print(f"File {page}.csv appended with files: {files_just_uploaded}")

