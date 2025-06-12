from typing import Literal

from pydantic import BaseModel


class Common(BaseModel):
    code: int
    type: Literal["unknown"]
    message: str
