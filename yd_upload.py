import requests
import json
from tqdm import tqdm


class YaUploader:
    HOST = 'https://cloud-api.yandex.net'

    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }

    def _get_upload_link(self, path):
        uri = '/v1/disk/resources/upload/'
        request_url = self.HOST + uri
        params = {'path': path, 'overwrite': True}
        response = requests.get(request_url, headers=self.get_headers(), params=params)
        return response.json()['href']

    def create_folder(self):

        uri = '/v1/disk/resources/'
        request_url = self.HOST + uri
        path = input('Введите название новой папки\n')
        params = {'path': path}
        response = requests.put(request_url, headers=self.get_headers(), params=params)
        if response.status_code == 409:
            check_folder_exists = input('Такая папка уже существует, продолжить загрузку в эту папку? Y/N\n').lower()
            if check_folder_exists == 'n':
                exit()
        return path

    def upload(self):

        uri = '/v1/disk/resources/upload/'
        request_url = self.HOST + uri
        path = self.create_folder()

        with open('Result.json', 'r') as f:
            result = (f.read())
            result = json.loads(result)
            for i in tqdm(result):
                file_name = i['file_name']
                link_for_upload = i['max_size_link']
                params = {'path': f'/{path}/' + file_name + '.jpg', 'url': link_for_upload}
                response = requests.post(request_url, params=params, headers=self.get_headers())

                if response.status_code != 202:
                    print('Ошибка загрузки')
        print('Загружено')
