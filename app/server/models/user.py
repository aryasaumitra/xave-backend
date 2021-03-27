from pydantic import BaseModel,Field,EmailStr
from typing import Optional
from datetime import datetime

class UserInfoSchema(BaseModel):
    
    firstName: str = Field(...)
    lastName: str =Field(...)
    emailID: EmailStr =Field(...)
    dateOfBirth: datetime.date =Field(...)

    class Config:
        schema_extra={
            "example":{
                "firstName":"John",
                "lastName":"Wick",
                "emailID":"johnwick@gmail.com"
            }
        }

class UserCreateSchema(UserInfoSchema):

    password: str =Field(...)


class UserDBSchema(UserInfoSchema):

    hashed_password: str= Field(...)

class UpdateUserSchema(BaseModel):

    firstName: Optional[str]
    lastName: Optional[str]
    emailID: Optional[EmailStr]
    dateOfBirth: Optional[datetime.date]