from copy import deepcopy

import allure

import cfg
from data.files.user import post_user
from data.models.common import Common
from data.models.users.model import User
from utils.allure.steps import CommonSteps


@allure.label("platform", "Автотесты")
@allure.label("module", "API")
@allure.label("feature", "Petstore API")
@allure.label("part", "Операции пользователя")
class TestUser:
    USER_ID = cfg.USER_ID
    USER_NAME = cfg.USER_NAME
    USER_PASSWORD = cfg.USER_PASSWORD

    @allure.id("12")
    @allure.title("Проверить создание пользователя")
    def test_post_user(self, api):
        with allure.step(CommonSteps.CREATE_USER):
            response = api.petstore.post_user({**deepcopy(post_user.body),
                                               "id": self.USER_ID,
                                               "username": self.USER_NAME,
                                               "password": self.USER_PASSWORD})
            with allure.step(CommonSteps.VERIFY_API_RESPONSE):
                response_json = api.petstore.valid_json(response)
                Common.model_validate(response_json)
                assert response_json["message"] == str(self.USER_ID)

    @allure.id("13")
    @allure.title("Проверить получение пользователя")
    def test_get_user_by_user_name(self, api):
        with allure.step(CommonSteps.CREATE_USER):
            response = api.petstore.post_user({**deepcopy(post_user.body),
                                               "id": self.USER_ID,
                                               "username": self.USER_NAME,
                                               "password": self.USER_PASSWORD})
            with allure.step(CommonSteps.VERIFY_API_RESPONSE):
                response_json = api.petstore.valid_json(response)
                assert response_json["message"] == str(self.USER_ID)
        with allure.step(CommonSteps.GET_USER):
            response_json = api.petstore.get_valid_user_by_user_name(self.USER_NAME)
            with allure.step(CommonSteps.VERIFY_API_RESPONSE):
                User.model_validate(response_json)
                assert response_json["id"] == int(self.USER_ID)
                assert response_json["username"] == self.USER_NAME
                assert response_json["password"] == self.USER_PASSWORD

    @allure.id("14")
    @allure.title("Проверить удаление пользователя")
    def test_delete_user_by_user_name(self, api):
        """ Тест стабилен, если запускать одиночно.
            Если запустить весь тестовый класс pytest tests/test_user.py, то тест превращается в флаки.
            Кривая API, кривая БД  ¯\_(ツ)_/¯
        """
        with allure.step(CommonSteps.CREATE_USER):
            response = api.petstore.post_user({**deepcopy(post_user.body),
                                               "id": self.USER_ID,
                                               "username": self.USER_NAME,
                                               "password": self.USER_PASSWORD})
            with allure.step(CommonSteps.VERIFY_API_RESPONSE):
                response_json = api.petstore.valid_json(response)
                assert response_json["message"] == str(self.USER_ID)
        with allure.step(CommonSteps.GET_USER):
            response_json = api.petstore.get_valid_user_by_user_name(self.USER_NAME)
            with allure.step(CommonSteps.VERIFY_API_RESPONSE):
                User.model_validate(response_json)
                assert response_json["id"] == int(self.USER_ID)
                assert response_json["username"] == self.USER_NAME
                assert response_json["password"] == self.USER_PASSWORD
        with allure.step(CommonSteps.DELETE_USER):
            response_json = api.petstore.delete_valid_user_by_user_name(self.USER_NAME)
            with allure.step(CommonSteps.VERIFY_API_RESPONSE):
                Common.model_validate(response_json)
                assert response_json["message"] == self.USER_NAME
        with allure.step(CommonSteps.GET_USER):
            response = api.petstore.get_user_by_user_name(self.USER_NAME)
            with allure.step(CommonSteps.VERIFY_API_RESPONSE):
                response_json = api.petstore.valid_json(response, 404)
                assert response_json["message"] == "User not found"
