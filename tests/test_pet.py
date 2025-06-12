import datetime
import time
from copy import deepcopy

import allure
import pytest
from loguru import logger

from data.files.pet import post_pet
from data.models.pets.model import PetList, PetDict
from data.models.common import Common
from helpers.api.client import Api
from utils.allure.steps import CommonSteps


@allure.label("platform", "Автотесты")
@allure.label("module", "API")
@allure.label("feature", "Petstore API")
@allure.label("part", "Питомцы")
class TestPets:

    @pytest.mark.parametrize("status", [
        pytest.param("available", marks=allure.id("1")),
        pytest.param("pending", marks=allure.id("2")),
        pytest.param("sold", marks=allure.id("3")),
    ])
    def test_get_by_status(self, api, status):
        allure.dynamic.title(f"Проверить получение питомца по статусу: {status}")
        with allure.step(f"Выполнить запрос получения питомца со status: {status}"):
            response = api.petstore.get_find_by_status(status)
        with allure.step(CommonSteps.VERIFY_API_RESPONSE):
            response_json = api.petstore.valid_json(response)
            logger.debug(response_json)
            PetList.model_validate(response_json)

    @pytest.mark.parametrize("pet_id, status", [
        pytest.param(555445, "available", marks=allure.id("4")),
        pytest.param(555446, "pending", marks=allure.id("5")),
        pytest.param(555447, "sold", marks=allure.id("6"))
    ])
    def test_post_pet(self, api, pet_id, status):
        allure.dynamic.title(f"Проверить создание питомца с id: {pet_id} и статусом: {status}")
        with allure.step(f"{CommonSteps.CREATE_PET} с id: {pet_id} и статусом: {status}"):
            response = api.petstore.post_pet({**deepcopy(post_pet.body),
                                              "id": pet_id,
                                              "status": status})
            with allure.step(CommonSteps.VERIFY_API_RESPONSE):
                response_json = api.petstore.valid_json(response)
                PetDict.model_validate(response_json)
                assert response_json["id"] == pet_id
                assert response_json["status"] == status

    @pytest.mark.parametrize("pet_id, status", [
        pytest.param(555445, "available", marks=allure.id("7")),
        pytest.param(555446, "pending", marks=allure.id("8")),
        pytest.param(555447, "sold", marks=allure.id("9"))
    ])
    def test_get_by_id(self, api, pet_id, status):
        allure.dynamic.title(f"Проверить получение питомца по идентификатору: {pet_id}")
        with allure.step(f"{CommonSteps.CREATE_PET} с id: {pet_id}"):
            response = api.petstore.post_pet({**deepcopy(post_pet.body),
                                              "id": pet_id,
                                              "status": status})
            with allure.step(CommonSteps.VERIFY_API_RESPONSE):
                response_json = api.petstore.valid_json(response)
                assert response_json["id"] == pet_id
        with allure.step(f"{CommonSteps.GET_PET} по id: {pet_id}"):
            response_json = api.petstore.get_valid_pet_by_id(pet_id)
            assert response_json["id"] == pet_id
            assert response_json["status"] == status

    @allure.id("10")
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

    @allure.id("11")
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
            response_json = api.petstore.delete_valid_pet_by_id(pet_id)
            assert response_json == {"code": 200, "type": "unknown", "message": f"{test_id}"}
