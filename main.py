import os
from pprint import pprint
from my_tokens import VK_TOKEN, YA__DISK_TOKEN
from ya_disk_uploader import YaUploader
import requests
import json


class VK:
    URL = 'https://api.vk.com/method/'
    METHOD_GET_USERS = 'users.get'
    METHOD_GET_PHOTOS = 'photos.get'
    PHOTO_INFO_PATH = os.getcwd()
    PHOTO_INFO_FILE_NAME = 'photo_info.json'

    def __init__(self, access_token, user_id, version='5.131'):
        self.token = access_token
        self.id = user_id
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}

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

    def get_photos_url(self):
        """Получает url для загрузки фотографий на яндекс диск"""


    def save_photo_info(self):
        """Сохраняет информацию о фотографии в json-формате"""
        photos_info = self.get_photos_info()
        photos_data = []

        if photos_info['response']['count']:
            for photo in photos_info['response']['items']:
                if photos_data:
                    for data in photos_data:
                        photo_info = {'file_name': photo['likes']['count']}

                        width = 0
                        height = 0
                        for size in photo['sizes']:
                            if (size['height'] * size['width']) > (width * height):
                                width = size['width']
                                height = size['height']

                        photo_info['size'] = f'{width}x{height}'
                        photos_data.append(photo_info)


if __name__ == '__main__':
    access_token = VK_TOKEN
    ya_disk_token = YA__DISK_TOKEN
    user_id = '749333920'

    vk = VK(access_token, user_id)
    uploader = YaUploader(ya_disk_token)

    pprint(vk.get_photos_info())
