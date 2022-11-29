from my_tokens import YA_DISK_TOKEN
import requests
import os


class YaUploader:
    URL_UPLOAD = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
    URL_DISK_INFO = 'https://cloud-api.yandex.net/v1/disk/resources'

    def __init__(self, token: str):
        self.token = token

    @property
    def header(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }

    def _get_upload_link(self, ya_disk_path: str, url_file_path: str = None) -> str:
        """Получает ссылку для загрузки файлов на Я.Диск"""
        params = {'path': ya_disk_path,
                  'overwrite': 'true', }

        if url_file_path:
            params['url'] = url_file_path

        response = requests.get(self.URL_UPLOAD, params=params, headers=self.header)

        if response.status_code == 200:
            url_upload = response.json().get('href')
            return url_upload

        return f'Error {response.status_code}.'

    def upload(self, ya_disk_path: str, file_path: str = None, url_file_path: str = None) -> int:
        """Загружает файлы на яндекс диск"""
        url_upload = self._get_upload_link(ya_disk_path)

        if file_path:
            files = {'file': open(file_path, 'rb')}
            response = requests.put(url_upload, files=files)
            return response.status_code

        if url_file_path:
            response = requests.post(url_upload)
            return response.status_code

    def disk_files(self):
        params = {
            'path': './',
            }
        response = requests.get(self.URL_DISK_INFO, params=params, headers=self.header)
        return response.json()


if __name__ == '__main__':
    # Получить путь к загружаемому файлу и токен от пользователя
    file_name = 'my_file.txt'
    path_to_file = os.path.join(os.path.expanduser('~'), f'Desktop\\{file_name}')
    token = YA_DISK_TOKEN
    uploader = YaUploader(token)
    result = uploader.upload(ya_disk_path=file_name, file_path=path_to_file)
    print(result)
