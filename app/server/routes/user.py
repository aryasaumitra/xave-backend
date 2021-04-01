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

#Create a User
@router.post("/signup",response_description="User Added Successfully to database")
async def create_new_user(user:UserCreateSchema=Body(...)):

    existing_user= await get_user_by_email(user.emailID)

    if existing_user:
        return ErrorResponseModel("An Error Occured",404,"Email ID already exists")
    else:
        hashed_password=bcrypt.hashpw(user.password.encode('utf=8'),bcrypt.gensalt())
        db_user=UserDBSchema(
            hashedPassword=hashed_password,
            firstName=user.firstName,
            lastName=user.lastName,
            emailID=user.emailID,
            dateOfBirth=user.dateOfBirth)

        db_user_data=jsonable_encoder(db_user)

        new_user=await add_user(db_user_data)

        if new_user:
            return ResponseModel(new_user,"User Added Successfully")
        return ErrorResponseModel("An Error Occured",404,"Unable to add User")

#Update a user
@router.patch("/update",response_description="User Data Updated Successfully")
async def update_user(email:str=Body(...),data:UpdateUserSchema=Body(...)):

    existing_user=await get_user_by_email(email)

    if existing_user:

        updated_user= await update_user_by_email(email=email,data=data)
        if updated_user:
            return ResponseModel("User Data Updated Successfully")
        return ErrorResponseModel("An Error Occured",403,"Unable to update User")

    else:
        return ErrorResponseModel("An Error Occured",404,"No User Found")

#Delete a user
@router.delete("/delete",response_description="User Deleted")
async def delete_user_profile(email:str=Body(...)):

    deleted_user=await delete_user(email)
    if deleted_user:
        return ResponseModel("User Deleted")
    return ErrorResponseModel("Internal Server Error",500,"Unable to delete user")