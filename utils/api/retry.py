from functools import wraps
from time import sleep

from loguru import logger
from requests import Response

STATUS_CODES_5XX = (500, 501, 502, 503, 504, 505)


def retry(attempts: int = 3, timeout: int = 3, status_codes: tuple = None):
    status_codes = status_codes or STATUS_CODES_5XX

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(attempts):
                try:
                    response: Response = func(*args, **kwargs)
                    if response.status_code in status_codes:
                        raise Exception(f"Unexpected status_code: {response.status_code}")
                    break
                except Exception as e:
                    logger.exception(f"Attempt #{i + 1}: {e}")
                    sleep(timeout)
            else:
                raise Exception(f"The number of {attempts=} to get valid response has been exceeded")
            return response

        return wrapper

    return decorator
