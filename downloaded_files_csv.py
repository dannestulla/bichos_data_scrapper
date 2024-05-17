import csv


def create_csv_file(file_name, files_list):
    with open(file_name + '.csv', 'w', newline='') as csv_file:
        csv_writter = csv.writer(csv_file)
        for string in files_list:
            csv_writter.writerow([string.split("\\")[-2] + "/" + string.split("\\")[-1]])
    print(f"Arquivo {file_name}+'.csv' salvo com sucesso.")
    return files_list


def read_csv_file(file_name, files_list):
    files_list = []
    new_file_name = file_name
    try:
        if file_name.endswith(".csv") == False:
            new_file_name = new_file_name+".csv"
        with open(new_file_name, 'r', newline='') as csv_file:
            csv_reader = csv.reader(csv_file)
            for line in csv_reader:
                files_list.append(line[0])

        print(files_list)
        return files_list
    except FileNotFoundError:
        create_csv_file(file_name, files_list)
        return files_list


def write_files_downloaded_to_csv(files_just_uploaded, page):
    current_file_data = read_csv_file(page + ".csv", files_just_uploaded)
    with open(page + '.csv', 'w', newline='') as csv_file:
        csv_writter = csv.writer(csv_file)
        for file in files_just_uploaded:
            csv_writter.writerow([file])
        for file in current_file_data:
            csv_writter.writerow([file])
    print(f"Arquivo {page}.csv gravado")
