from settings import VK_TOKEN, YD_TOKEN
import vk_get_photos
import yd_upload


if __name__ == '__main__':
    user_id = input('Введите id пользователя\n')
    count_photos = input('Введите количество скачиваемых фото\n')
    vk_client = vk_get_photos.VkPhoto(VK_TOKEN, '5.131')
    vk_client.get_photos(user_id, count_photos)

    yd_upload.YaUploader(YD_TOKEN).upload()