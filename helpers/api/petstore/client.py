from typing import Any, Literal
from urllib.parse import urljoin

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
        url = self.build_url(f"pet/{pet_id}")
        return self.session.get(url)

    def put_existing_pet(self, request_body: dict) -> Response:
        url = self.build_url("pet")
        return self.session.put(url, json=request_body)

    def delete_existing_pet(self, pet_id: int) -> Response:
        url = self.build_url(f"pet/{pet_id}")
        return self.session.delete(url)
