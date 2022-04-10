from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    email_id: str
    password: str


class NewUser(BaseModel):
    full_name: str
    email_id: str
    password: str


class UserDetails(BaseModel):
    age: int
    gender: str
    height: int
    weight: int
    activity: list
    medical: list
