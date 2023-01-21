import requests


class VkPhoto:
    HOST = 'https://api.vk.com/method/'

    def __init__(self, token, version, user_ids, count=5):
        self.user_ids = user_ids
        self.count = count
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

    def get_photos(self):
        user_info = self.get_user(self.user_ids)
        name = f"{user_info['response'][0]['first_name']} {user_info['response'][0]['last_name']}"
        get_photo_url = self.HOST + 'photos.get'
        get_photo_params = {
            'owner_id': self.user_ids,
            'album_id': 'profile',
            'extended': '1',
            'photo_sizes': '1',
            'count': self.count
        }
        result = requests.get(get_photo_url, params={**self.params, **get_photo_params}).json()
        if 'error' in result:
            error = result['error']['error_msg']
            print(f'Ошибка: {error}')
            exit()
        elif result['response']['count'] == 0:
            print(f'У пользователя {name} нет фото')
            exit()
        else:
            return result
