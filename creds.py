import requests
import configparser
import base64

def get_upload_request_id(owner, repo, HEADER):
    url = f'https://api.github.com/repos/{owner}/{repo}/content_uploads'
    response = requests.post(url, headers=HEADER)
    response.raise_for_status()
    return response.json()['upload_id']

def upload_chunks(owner, repo, upload_id, file_path, offset, chunk_size, HEADER):
    url = f'https://api.github.com/repos/{owner}/{repo}/content_uploads/{upload_id}'
    headers = {
        'accept': 'application/json;version=2',
    }
    with open(file_path, 'rb') as file:
        file.seek(offset)
        chunk = file.read(chunk_size)
    files = {
        'offset': str(offset),
        'content': chunk,
    }
    response = requests.put(url, headers=headers, files=files)
    response.raise_for_status()

def import_upload(owner, repo, upload_id, HEADER):
    url = f'https://api.github.com/repos/{owner}/{repo}/import_uploads'
    data = {
        'upload_ids': [upload_id],
    }
    response = requests.put(url, json=data, headers=HEADER)
    response.raise_for_status()

def delete_upload(owner, repo, upload_id, HEADER):
    url = f'https://api.github.com/repos/{owner}/{repo}/content_uploads/{upload_id}'
    response = requests.delete(url, headers=HEADER)
    response.raise_for_status()

def main():
    config = configparser.ConfigParser()
    config.read('secrets.ini')
    TOKEN = config.get('github', 'token')
    OWNER = config.get('github', 'owner')
    HEADER = {
        'Authorization': f'token {TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }

    repo_name = input("Enter the name of the repository to upload files to: ")
    file_path = 'requirements.txt'  # Update with your file path
    chunk_size = 5242880  # 5MB chunk size, adjust as needed

    upload_id = get_upload_request_id(OWNER, repo_name, HEADER)
    offset = 0
    with open(file_path, 'rb') as file:
        file_size = file.seek(0, 2)
        while offset < file_size:
            upload_chunks(OWNER, repo_name, upload_id, file_path, offset, chunk_size, HEADER)
            offset += chunk_size

    import_upload(OWNER, repo_name, upload_id, HEADER)
    delete_upload(OWNER, repo_name, upload_id, HEADER)
    print("File uploaded successfully!")

if __name__ == "__main__":
    main()
