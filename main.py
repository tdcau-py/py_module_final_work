from pprint import pprint
from datetime import datetime
from my_tokens import VK_TOKEN, YA_DISK_TOKEN
from ya_disk_uploader import YaUploader
import requests
import json
import os


class VK:
    URL = 'https://api.vk.com/method/'
    METHOD_GET_USERS = 'users.get'
    METHOD_GET_PHOTOS = 'photos.get'
    PHOTO_INFO_PATH = os.getcwd()
    PHOTO_INFO_FILE_NAME = 'photo_info.json'
    VK_API_VERSION = '5.131'
    ACCESS_TOKEN = VK_TOKEN

    def __init__(self, user_id: str, yandex_disk_token: str = None):
        self.yandex_token = yandex_disk_token
        self.id = user_id
        self.params = {'access_token': self.ACCESS_TOKEN, 'v': self.VK_API_VERSION}

    def _get_url(self, method: str) -> str:
        """Формирует url-адрес с передачей метода """
        return f'{self.URL}{method}'

    def users_info(self) -> json:
        """Отправляет запрос на получение данных о пользователе"""
        url = self._get_url(self.METHOD_GET_USERS)
        params = {'user_ids': self.id}
        response = requests.get(url, params={**self.params, **params})
        return response.json()

    def get_photos_info(self) -> json:
        """Отправляет запрос на получение данных о фотографиях с профиля (аватарок)"""
        url = self._get_url(self.METHOD_GET_PHOTOS)
        params = {'album_id': 'profile', 'extended': '1', 'user_ids': self.id}
        response = requests.get(url, params={**self.params, **params})
        return response.json()

    def save_photo_info(self):
        """Сохраняет информацию о фотографии в json-формате"""
        photos_info = self.get_photos_info()
        photos_data = []

        if photos_info['response']['count']:
            for photo in photos_info['response']['items']:
                likes_photo = photo["likes"]["count"]
                name_photo = f'{likes_photo}.jpg'
                url_photo = ''
                width = 0
                height = 0

                for size in photo['sizes']:
                    if (size['height'] * size['width']) > (width * height):
                        width = size['width']
                        height = size['height']
                        url_photo = size['url']

                size = f'{width}x{height}'
                date_photo = datetime.fromtimestamp(photo['date']).date().isoformat()

                if photos_data:
                    for data in photos_data:
                        if name_photo == data['file_name']:
                            name_photo = f'{likes_photo}_{date_photo}.jpg'
                            break

                photo_info = {'file_name': name_photo, 'size': size}
                photos_data.append(photo_info)
                status_operation = self.upload_photos(name_photo, url_photo)

        with open('dump.json', 'w') as json_file:
            json.dump(photos_data, json_file)

        return status_operation

    def upload_photos(self, photo_name: str, download_url: str):
        """Загружает фотографии на яндекс диск"""
        uploader = YaUploader(self.yandex_token)
        result = uploader.upload(ya_disk_path=photo_name, url_file_path=download_url)
        return result


if __name__ == '__main__':
    user_id = '749333920'
    ya_disk_token = YA_DISK_TOKEN
    vk = VK(user_id, ya_disk_token)
    result = vk.save_photo_info()
    print(result)
