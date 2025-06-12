from pydantic import BaseModel, PositiveInt, NonNegativeInt


class User(BaseModel):
    id: PositiveInt
    username: str
    firstName: str
    lastName: str
    email: str
    password: str
    phone: str
    userStatus: NonNegativeInt
