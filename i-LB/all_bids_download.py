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
ids = {'1V6UF6-eB-u9e6DDHVdoQjX6mp_MAJhOd': 'test_bids_log.csv',
       '1qbq2T9s-_EU0138S9Y8s5lixjJaD3sEa': 'train_bids_log.csv',
       '1XR5WP385XZuLJK5-Hd3R72hSOLrJSq8Y': 'valid_bids_log.csv',
       '1rX0knEeTEPUDU-mG_Ts271-hC74vcm8D': 'test_bids_aws.csv',
       '1SQ7R-dutZLaKGNV9Cij710xA6ESxUi3I': 'train_bids_aws.csv',
       '13vQqV1-BczjG3_Nrzzn1UTYVCbACBmnw': 'valid_bids_aws.csv',
       '12ms4eRWhPlfzfvouW4gYsVDQWXSZ6wi_': 'test_bids.csv',
       '1BXQIE0HcxF5u4YT01emZbo5GKDTeuCe6': 'train_bids.csv',
       '1-paDXaBKN8Lv__km7ZsMxQmFfyeEpM9B': 'valid_bids.csv'}

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
