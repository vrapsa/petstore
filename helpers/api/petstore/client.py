import datetime
import time
from typing import Any, Literal
from urllib.parse import urljoin

import pytest
from loguru import logger
from requests import Response

from utils.api.session import SessionApi


class PetstoreApi:
    SERVER = "v2"

    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = SessionApi()
        self.session.headers["Content_Type"] = "application/json"

    def build_url(self, url_part: str) -> str:
        return urljoin(self.base_url, f"{self.SERVER}/{url_part}")

    @staticmethod
    def valid_json(response: Response, expected_code: int = 200) -> Any:
        if response.status_code == expected_code:
            return response.json()
        else:
            raise Exception(f"Unexpected status code: {response.status_code} \n Expected status_code: {expected_code}")

    def get_find_by_status(self, params: Literal["available", "pending", "sold"]) -> Response:
        params = {"status": params}
        url = self.build_url("pet/findByStatus")
        return self.session.get(url, params=params)

    def post_pet(self, request_body: dict) -> Response:
        url = self.build_url("pet")
        return self.session.post(url, json=request_body)

    def get_pet_by_id(self, pet_id: int) -> Response:
        """ Настоящий метод, который должен использоваться для получения ID питомца"""
        url = self.build_url(f"pet/{pet_id}")
        return self.session.get(url)

    def get_valid_pet_by_id(self, pet_id: int) -> Response:
        """ Костыльный метод настоящего метода get_pet_by_id.
            Функция выполняет обход некорректной работы API.
            Метод GET /pet/{petId} периодически возвращает 404, несмотря на то,
            что такой pet_id существует.
            На реальном проекте, конечно, никакие обходы не нужны, т.к. если
            подстраивать автотесты под каждую ошибку, то в автотестах нет смысла. """
        start_time = datetime.datetime.now()
        timeout = datetime.timedelta(seconds=15)
        while datetime.datetime.now() - start_time < timeout:
            response = PetstoreApi.get_pet_by_id(self, pet_id)
            if response.status_code == 200:
                response_json = PetstoreApi.valid_json(response)
                return response_json
            else:
                logger.debug(f"Unexpected status code: {response.status_code}")
                time.sleep(1)
                continue
        return pytest.fail(reason="Pet is not found.")

    def put_existing_pet(self, request_body: dict) -> Response:
        url = self.build_url("pet")
        return self.session.put(url, json=request_body)

    def delete_existing_pet(self, pet_id: int) -> Response:
        """ Настоящий метод, который должен использоваться для получения ID питомца"""
        url = self.build_url(f"pet/{pet_id}")
        return self.session.delete(url)

    def delete_valid_pet_by_id(self, pet_id: int) -> dict:
        """ Костыльный метод настоящего метода delete_existing_pet.
            Функция выполняет обход некорректной работы API.
            Метод DELETE /pet/{petId} периодически возвращает 404, несмотря на то,
            что такой pet_id существует.
            На реальном проекте, конечно, никакие обходы не нужны, т.к. если
            подстраивать автотесты под каждую ошибку, то в автотестах нет смысла. """
        start_time = datetime.datetime.now()
        timeout = datetime.timedelta(seconds=15)
        while datetime.datetime.now() - start_time < timeout:
            response = PetstoreApi.delete_existing_pet(self, pet_id)
            if response.status_code == 200:
                response_json = PetstoreApi.valid_json(response)
                return response_json
            else:
                logger.debug(f"Unexpected status code: {response.status_code}")
                time.sleep(1)
                continue
        return pytest.fail(reason="Pet is not found.")

    def post_user(self, request_body: dict) -> Response:
        url = self.build_url("user")
        return self.session.post(url, json=request_body)
