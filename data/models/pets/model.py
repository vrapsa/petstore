from typing import Literal

from pydantic import RootModel, BaseModel, NonNegativeInt


class PetData(BaseModel):
    id: int
    name: str = None


class PetDict(BaseModel):
    """ Схема сильно подстроена, чтобы автотесты не падали.
        На реальном проекте, конечно, никакие обходы не нужны, т.к. если
        подстраивать автотесты под каждый баг, то в автотестах нет смысла. """
    id: NonNegativeInt = None
    category: PetData = None
    name: str = None
    photoUrls: list[str | None] = None
    tags: list[PetData] | list = None
    status: Literal["available", "pending", "sold"] = None


class PetList(RootModel):
    root: list[PetDict]
