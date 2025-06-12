from curlify2 import Curlify
from loguru import logger
from requests import Session, Response

from utils.api.retry import retry


class SessionApi(Session):

    def __init__(self):
        super().__init__()

    def request(self, method: str, url: str, **kwargs) -> Response:
        response = super().request(method, url, **kwargs)
        logger.debug(f"Request cURL: {Curlify(response.request).to_curl()}")
        logger.debug(f"Response status code: {response.status_code}")
        logger.debug(f"Response time: {response.elapsed}")
        return response

    @retry(attempts=3, timeout=3)
    def get(self, url, **kwargs) -> Response:
        return super().get(url, **kwargs)

    @retry(attempts=3, timeout=3)
    def post(self, url, **kwargs) -> Response:
        return super().post(url, **kwargs)

    @retry(attempts=3, timeout=3)
    def put(self, url, **kwargs) -> Response:
        return super().put(url, **kwargs)

    @retry(attempts=3, timeout=3)
    def patch(self, url, **kwargs) -> Response:
        return super().patch(url, **kwargs)

    @retry(attempts=3, timeout=3)
    def delete(self, url, **kwargs) -> Response:
        return super().delete(url, **kwargs)
