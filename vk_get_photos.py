import json
import requests
import datetime as dt


class VkPhoto:
    HOST = 'https://api.vk.com/method/'

    def __init__(self, token, version):
        self.params = {
            'access_token': token,
            'v': version
        }

    def get_user(self, user_ids):
        get_user_url = self.HOST + 'users.get'
        get_user_params = {
            'user_ids': user_ids
        }
        user_info = requests.get(get_user_url, params={**self.params, **get_user_params}).json()
        return user_info

    def get_photos(self, user_ids, count=5):
        user_info = self.get_user(user_ids)
        name = f"{user_info['response'][0]['first_name']} {user_info['response'][0]['last_name']}"
        get_photo_url = self.HOST + 'photos.get'
        get_photo_params = {
            'owner_id': user_ids,
            'album_id': 'profile',
            'extended': '1',
            'photo_sizes': '1',
            'count': count
        }
        res = requests.get(get_photo_url, params={**self.params, **get_photo_params}).json()
        if 'error' in list(res):
            error = res['error']['error_msg']
            return error
        if res['response']['count'] == 0:
            print(f'У пользователя {name} нет фото')
            exit()

        list_photos = []
        list_likes = []
        upload_date = dt.date.today().strftime('%d.%m.%Y')

        print(f'Загружаем фото пользователя: {name}')
        for group in (res['response']['items']):
            if group['likes']['count'] in list_likes:
                list_photos.append(
                    {
                        'file_name': f"{group['likes']['count']} - {upload_date}.jpeg",
                        'size': group['sizes'][-1]['type'],
                        'max_size_link': group['sizes'][-1]['url']
                    }
                )
            else:
                list_photos.append(
                    {
                        'file_name': f"{group['likes']['count']}.jpeg",
                        'size': group['sizes'][-1]['type'],
                        'max_size_link': group['sizes'][-1]['url']
                    }
                )
            list_likes.append(group['likes']['count'])

        with open('Result.json', 'w') as file:
            json.dump(list_photos, file)
        return list_photos
