import datetime
import time
from copy import deepcopy

import allure
import pytest
from loguru import logger

from data.files.pets import post_pet
from data.models.pets.model import PetList, PetDict
from data.models.common import Common
from helpers.api.client import Api
from utils.allure.steps import CommonSteps


class TestPets:
    PET_STATUS = ["available", "pending", "sold"]
    PARAMETRIZE = [
        (555445, "available"),
        (555446, "pending"),
        (555447, "sold")
    ]

    @staticmethod
    def get_valid_pet_by_id(pet_id: int) -> dict:
        """ Функция выполняет обход некорректной работы API.
            Метод GET /pet/{petId} периодически возвращает 404, несмотря на то,
            что такой pet_id существует.
            На реальном проекте, конечно, никакие обходы не нужны, т.к. если
            подстраивать автотесты под каждую ошибку, то в автотестах нет смысла. """
        api = Api()
        start_time = datetime.datetime.now()
        timeout = datetime.timedelta(seconds=15)
        while datetime.datetime.now() - start_time < timeout:
            response = api.petstore.get_pet_by_id(pet_id)
            if response.status_code == 200:
                with allure.step(CommonSteps.VERIFY_API_RESPONSE):
                    response_json = api.petstore.valid_json(response)
                    PetDict.model_validate(response_json)
                    return response_json
            else:
                logger.debug(f"Unexpected status code: {response.status_code}")
                time.sleep(1)
                continue
        return pytest.fail(reason="Pet is not found.")

    @staticmethod
    def delete_pet_by_id(pet_id: int) -> dict:
        """ Функция выполняет обход некорректной работы API.
            Метод DELETE /pet/{petId} периодически возвращает 404, несмотря на то,
            что такой pet_id существует.
            На реальном проекте, конечно, никакие обходы не нужны, т.к. если
            подстраивать автотесты под каждую ошибку, то в автотестах нет смысла. """
        api = Api()
        start_time = datetime.datetime.now()
        timeout = datetime.timedelta(seconds=15)
        while datetime.datetime.now() - start_time < timeout:
            response = api.petstore.delete_existing_pet(pet_id)
            if response.status_code == 200:
                with allure.step(CommonSteps.VERIFY_API_RESPONSE):
                    response_json = api.petstore.valid_json(response)
                    Common.model_validate(response_json)
                    return response_json
            else:
                logger.debug(f"Unexpected status code: {response.status_code}")
                time.sleep(1)
                continue
        return pytest.fail(reason="Pet is not found.")

    @allure.id("1")
    @allure.title("Проверить получения питомца по статусу")
    @pytest.mark.parametrize("status", [
        status for status in PET_STATUS
    ])
    def test_get_by_status(self, api, status):
        with allure.step(f"Выполнить запрос получения питомца со status: {status}"):
            response = api.petstore.get_find_by_status(status)
        with allure.step(CommonSteps.VERIFY_API_RESPONSE):
            response_json = api.petstore.valid_json(response)
            logger.debug(response_json)
            PetList.model_validate(response_json)

    @allure.id("2")
    @allure.title("Проверить создание питомца")
    @pytest.mark.parametrize("pet_id, status", PARAMETRIZE)
    def test_post_pet(self, api, pet_id, status):
        with allure.step(f"{CommonSteps.CREATE_PET} с id: {pet_id} и статусом: {status}"):
            response = api.petstore.post_pet({**deepcopy(post_pet.body),
                                              "id": pet_id,
                                              "status": status})
            with allure.step(CommonSteps.VERIFY_API_RESPONSE):
                response_json = api.petstore.valid_json(response)
                PetDict.model_validate(response_json)
                assert response_json["id"] == pet_id
                assert response_json["status"] == status

    @allure.id("3")
    @allure.title("Проверить получение питомца по идентификатору")
    @pytest.mark.parametrize("pet_id, status", PARAMETRIZE)
    def test_get_by_id(self, api, pet_id, status):
        with allure.step(f"{CommonSteps.CREATE_PET} с id: {pet_id} и статусом: {status}"):
            response = api.petstore.post_pet({**deepcopy(post_pet.body),
                                              "id": pet_id,
                                              "status": status})
            with allure.step(CommonSteps.VERIFY_API_RESPONSE):
                response_json = api.petstore.valid_json(response)
                assert response_json["id"] == pet_id
        with allure.step(f"{CommonSteps.GET_PET} по id: {pet_id}"):
            response_json = TestPets.get_valid_pet_by_id(pet_id)
            assert response_json["id"] == pet_id
            assert response_json["status"] == status

    @allure.id("4")
    @allure.title("Проверить обновление питомца")
    def test_put_existing_pet(self, api):
        with allure.step(CommonSteps.PREPARE_TEST_DATA):
            pet_id = 555448
            pet_status = "available"
        with allure.step(CommonSteps.CREATE_PET):
            response = api.petstore.post_pet({**deepcopy(post_pet.body),
                                              "id": pet_id,
                                              "status": pet_status})
            with allure.step(CommonSteps.VERIFY_API_RESPONSE):
                response_json = api.petstore.valid_json(response)
                assert response_json["id"] == pet_id
                assert response_json["status"] == pet_status
                pet_name = response_json["name"]
        with allure.step(f"{CommonSteps.UPDATE_PET} с id: {pet_id}"):
            response = api.petstore.put_existing_pet({**deepcopy(post_pet.body),
                                                      "id": 555448,
                                                      "status": pet_status,
                                                      "name": "Updated Seven"})
            with allure.step(CommonSteps.VERIFY_API_RESPONSE):
                response_json = api.petstore.valid_json(response)
                PetDict.model_validate(response_json)
                assert response_json["id"] == pet_id
                assert response_json["status"] == pet_status
                assert response_json["name"] == "Updated Seven" != pet_name

    @allure.id("5")
    @allure.title("Проверить удаление питомца")
    def test_delete_pet(self, api):
        with allure.step(CommonSteps.PREPARE_TEST_DATA):
            test_id = 555449
            test_status = "available"
        with allure.step(CommonSteps.CREATE_PET):
            response = api.petstore.post_pet({**deepcopy(post_pet.body),
                                              "id": test_id,
                                              "status": test_status})
            with allure.step(CommonSteps.VERIFY_API_RESPONSE):
                response_json = api.petstore.valid_json(response)
                pet_id = response_json["id"]
                assert pet_id == test_id
                assert response_json["status"] == test_status
        with allure.step(f"{CommonSteps.DELETE_PET} + с id: {pet_id}"):
            response_json = TestPets.delete_pet_by_id(pet_id)
            assert response_json == {"code": 200, "type": "unknown", "message": f"{test_id}"}
