from settings import VK_TOKEN, YD_TOKEN
from vk_get_photos import VkPhoto
from yd_upload import YaUploader
import datetime as dt


def save_photo(user_ids, count):
    res = VkPhoto(VK_TOKEN, 5.131, user_ids, count).get_photos()
    list_photos = []
    list_likes = []
    upload_date = dt.date.today().strftime('%d.%m.%Y')

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
    return list_photos


if __name__ == '__main__':
    user_id = input('Введите id пользователя\n')
    count_photos = input('Введите количество скачиваемых фото\n')

    YaUploader(YD_TOKEN, save_photo(user_id, count_photos)).upload()
