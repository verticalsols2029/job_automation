from ninja import Schema
from pydantic import EmailStr

class RegisterIn(Schema):
    email: EmailStr
    password: str
    first_name: str
    last_name: str

class TokenOut(Schema):
    access: str
    refresh: str

class ErrorOut(Schema):
    message: str