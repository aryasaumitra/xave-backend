from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
import bcrypt

# Importing Database functions
from ..database.user import (
    add_user,
    get_user_by_email,
    update_user_by_email,
    delete_user
)

#Importing Response Models
from ..models.base import (
    ErrorResponseModel,
    ResponseModel
)

# Importing User Schema
from ..models.user import (
    UserCreateSchema,
    UserDBSchema,
    UpdateUserSchema
)

router =APIRouter()

@router.post("/",response_description="User Added Successfully to database")
async def create_new_user(user:UserCreateSchema=Body(...)):

    hashed_password=bcrypt.hashpw(user.password.encode('utf=8'),bcrypt.gensalt())
    db_user=UserDBSchema(hashedPassword=hashed_password,firstName=user.firstName,lastName=user.lastName,emailID=user.emailID)

    db_user_data=jsonable_encoder(db_user)

    new_user=await add_user(db_user_data)

    if new_user:
        return ResponseModel(new_user,"User Added Successfully")
    return ErrorResponseModel("An Error Occured",404,"Unable to add User")