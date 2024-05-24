from botocore.exceptions import NoCredentialsError
from model.credentials import bucket_name, folder_path


def upload_to_s3(list_images, page, s3_client):
    for image_file_name in list_images:
        file_name = image_file_name.split('/')[-1]
        file_path2 = folder_path+'database\\' + page + '\\' + file_name
        try:
            print("Uploading " + image_file_name)
            s3_client.upload_file(file_path2, bucket_name, image_file_name)
        except NoCredentialsError:
            print("Credenciais não disponíveis")
            return False


def upload_file_list_to_s3(page, s3_client):
    file_list_location = folder_path+"bichos_data_scrapper\\folders_content_csv\\" + page + ".csv"
    s3_client.upload_file(file_list_location, bucket_name, page + ".csv")
    print(f"Enviada lista de arquivos baixados da pagina {page}")