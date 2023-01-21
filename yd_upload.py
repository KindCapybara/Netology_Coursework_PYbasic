import requests
import json
from tqdm import tqdm


class YaUploader:
    HOST = 'https://cloud-api.yandex.net'

    def __init__(self, token, list_photos):
        self.token = token
        self.list_photos = list_photos

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
        list_photos_for_json = []
        path = self.create_folder()
        for photo in tqdm(self.list_photos):
            file_name = photo['file_name']
            size = photo['size']
            link_for_upload = photo['max_size_link']
            uri = '/v1/disk/resources/upload/'
            request_url = self.HOST + uri
            params = {'path': f'/{path}/' + file_name + '.jpg', 'url': link_for_upload}
            response = requests.post(request_url, params=params, headers=self.get_headers())

            if response.status_code != 202:
                print('Ошибка загрузки')
            list_photos_for_json.append(
                {
                    'file_name': file_name,
                    'size': size
                }
            )
        with open('Result.json', 'w') as file:
            json.dump(list_photos_for_json, file)
        print('Загружено')
