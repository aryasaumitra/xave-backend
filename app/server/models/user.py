from pydantic import BaseModel,Field,EmailStr
from typing import Optional
from datetime import date

class UserInfoSchema(BaseModel):
    
    firstName: str = Field(...)
    lastName: str =Field(...)
    emailID: EmailStr =Field(...)
    dateOfBirth: date =Field(...)

    class Config:
        schema_extra={
            "example":{
                "firstName":"John",
                "lastName":"Wick",
                "emailID":"johnwick@gmail.com",
                "dateOfBirth":"1997-10-22",
                "password":"password"
            }
        }

class UserCreateSchema(UserInfoSchema):

    password: str =Field(...)


class UserDBSchema(UserInfoSchema):

    hashedPassword: str= Field(...)

class UpdateUserSchema(BaseModel):

    firstName: Optional[str]
    lastName: Optional[str]
    dateOfBirth: Optional[date]

class UserLoginSchema(BaseModel):

    emailID: EmailStr=Field(...)
    password:str=Field(...)

    class Config:
        schema_extra={
            "example":{
                "emailID":"xyz@gmail.com",
                "password":"password"
            }
        }