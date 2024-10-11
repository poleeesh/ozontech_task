import random
from time import sleep

import allure
import pytest
import requests

YANDEX_DISK_URL = 'https://cloud-api.yandex.net/v1/disk/resources'
DOG_CEO_URL = 'https://dog.ceo/api/breed/'
TOKEN = 'y0_AgAAAABXEqcBAADLWwAAAAEUEQJYAAA25CY0aFpAmYBDwMJeAoggT0Vvog'
FOLDER_NAME = 'test_folder'
HEADERS = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': f'OAuth {TOKEN}'}

TEST_BREEDS = ['doberman', random.choice(['bulldog', 'collie'])]


class YaUploader:
    @staticmethod
    def create_folder(path: str) -> None:
        requests.put(f'{YANDEX_DISK_URL}?path={path}', headers=HEADERS)

    @staticmethod
    def upload_photos_to_yd(path: str, url_file: str, name: str) -> None:
        url = YANDEX_DISK_URL + "/upload"
        params = {"path": f'/{path}/{name}', 'url': url_file, "overwrite": "true"}
        requests.post(url, headers=HEADERS, params=params)

    @staticmethod
    def delete_photos_from_yd(path: str, name: str) -> None:
        params = {"path": f'/{path}/{name}', "permanently": "true"}
        requests.delete(YANDEX_DISK_URL, headers=HEADERS, params=params)

    @staticmethod
    def update_photos(path: str):
        params = {"path": f'/{path}/', "body": "{'custom_properties': {}}"}
        requests.patch(YANDEX_DISK_URL, headers=HEADERS, params=params)


class DogCeoApi:
    @staticmethod
    def get_sub_breeds(breed: str) -> list[str]:
        res = requests.get(f'{DOG_CEO_URL}{breed}/list')
        return res.json().get('message', [])

    @staticmethod
    def get_json_message(sub_path: str) -> str:
        res = requests.get(f"{DOG_CEO_URL}{sub_path}/images/random")
        return res.json().get('message')

    @staticmethod
    def get_urls(breed: str, sub_breeds: list[str]) -> list[str]:
        url_images = []
        if sub_breeds:
            for sub_breed in sub_breeds:
                url_images.append(DogCeoApi.get_json_message(f'{breed}/{sub_breed}'))
        else:
            url_images.append(DogCeoApi.get_json_message(breed))
        return url_images


class TestDogUpload:
    @pytest.fixture
    @allure.title("Upload photos through program to check")
    def upload_photos(self, breed):
        with allure.step("Upload photos"):
            sub_breeds = DogCeoApi.get_sub_breeds(breed)
            urls = DogCeoApi.get_urls(breed, sub_breeds)
            YaUploader.create_folder(FOLDER_NAME)
            for url in urls:
                part_name = url.split('/')[-2:]
                name = '_'.join(part_name)
                YaUploader.upload_photos_to_yd(FOLDER_NAME, url, name)
            YaUploader.update_photos(FOLDER_NAME)
            # даже после обновления ресурса методом /patch тест иногда не получал текущую информацию
            # так что пришлось добавить таймаут ¯\_(ツ)_/¯
            sleep(10)
        yield
        with allure.step("Delete photos"):
            for url in urls:
                part_name = url.split('/')[-2:]
                name = '_'.join(part_name)
                YaUploader.delete_photos_from_yd(FOLDER_NAME, name)

    @pytest.mark.parametrize('breed', TEST_BREEDS)
    @pytest.mark.usefixtures("upload_photos")
    @allure.title("Проверка программы для загрузки картинок собак")
    def test_proverka_upload_dog(self, breed):
        with allure.step("Get HTTP Response and assert info in it"):
            response = requests.get(f'{YANDEX_DISK_URL}?path=/{FOLDER_NAME}', headers=HEADERS).json()
            assert response['type'] == "dir"
            assert response['name'] == FOLDER_NAME

        with allure.step("Assert info about files in response"):
            response_items = response['_embedded']['items']
            sub_breeds = DogCeoApi.get_sub_breeds(breed)
            if not sub_breeds:
                assert len(response_items) == 1
            else:
                assert len(response_items) == len(sub_breeds)

            for item in response_items:
                assert item['type'] == 'file'
                assert item['name'].startswith(breed)
