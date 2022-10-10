import requests
import os


class YaUploader:
    URL_UPLOAD = 'https://cloud-api.yandex.net/v1/disk/resources/upload'

    def __init__(self, token: str):
        self.token = token

    @property
    def header(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }

    def _get_upload_link(self, ya_disk_path: str) -> str:
        """Получает ссылку для загрузки файлов на Я.Диск"""
        params = {'path': ya_disk_path,
                  'overwrite': 'true', }
        response = requests.get(self.URL_UPLOAD, params=params, headers=self.header)
        print(response.status_code)
        url_upload = response.json().get('href')

        return url_upload

    def upload(self, ya_disk_path: str, file_path: str) -> int:
        """Загружает файлы на яндекс диск"""
        url_upload = self._get_upload_link(ya_disk_path)
        files = {'file': open(file_path, 'rb')}
        response = requests.put(url_upload, files=files)

        return response.status_code


if __name__ == '__main__':
    # Получить путь к загружаемому файлу и токен от пользователя
    file_name = 'my_file.txt'
    path_to_file = os.path.join(os.path.expanduser('~'), f'Desktop\\{file_name}')
    token = ...
    uploader = YaUploader(token)
    result = uploader.upload(file_path=path_to_file, ya_disk_path=f'{file_name}')
    print(result)
