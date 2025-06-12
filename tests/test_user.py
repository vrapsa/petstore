from copy import deepcopy

import allure

import cfg
from data.files.user import post_user
from data.models.common import Common
from utils.allure.steps import CommonSteps


@allure.label("platform", "Автотесты")
@allure.label("module", "API")
@allure.label("feature", "Petstore API")
@allure.label("part", "Операции пользователя")
class TestUser:

    @allure.id("12")
    @allure.title("Проверить создание пользователя")
    def test_post_user(self, api):
        with allure.step(CommonSteps.PREPARE_TEST_DATA):
            user_id = cfg.USER_ID
            user_name = cfg.USER_NAME
            password = cfg.USER_PASSWORD
        with allure.step(CommonSteps.CREATE_USER):
            response = api.petstore.post_user({**deepcopy(post_user.body),
                                               "id": user_id,
                                               "username": user_name,
                                               "password": password})
            with allure.step(CommonSteps.VERIFY_API_RESPONSE):
                response_json = api.petstore.valid_json(response)
                Common.model_validate(response_json)
