import os
import requests

def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:
                f.write(chunk)

# Create a data folder
data_path = '../Data'
if not os.path.exists(data_path):
    os.makedirs(data_path)

# Define the urls
ids = {'1mbfAYjzLfk3tT0MT4L7X_ywMfyv2DGYQ': 'Group_xx.csv',
       '1CXUewoiTs94QhZ0Q02vSD3qM_K4-ZJsD': 'test.csv',
       '1jas8TNVs7D8m3AOmjE3KFRKNu0xRHF8x': 'validation.csv',
       '1-yV2eFMhhJW1qS2UpfKsuOlG4xjAhWVR': 'train.csv'}

# For every file in ids download it in the data folder
for cid in ids:

    # Define the file name
    csv_file = os.path.join(data_path, ids[cid])

    # Download the file if it does not exist
    if not os.path.isfile(csv_file):
        download_file_from_google_drive(cid, csv_file)
        print('File {} downloaded successfully!'.format(ids[cid]))
    else:
        print('File {} already exists!'.format(ids[cid]))
