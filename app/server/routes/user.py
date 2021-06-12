from ..auth.auth_bearer import JWTBearer
from fastapi.param_functions import Depends
from ..auth.auth_handler import create_jwt_token, decode_jwt
from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
import bcrypt

# Importing Database functions
from ..database.user import (
    add_user,
    get_user_by_email,
    update_user,
    delete_user,
    get_user_by_id
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
    UpdateUserSchema,
    UserLoginSchema
)

router =APIRouter()

#Helper Functions
async def CheckLogin(user:UserLoginSchema=Body(...)):
    
    existing_user=await get_user_by_email(user.emailID)
    # print(existing_user)
    # print(user)

    if existing_user:
        return bcrypt.checkpw(password=user.password.encode('utf-8'),hashed_password=existing_user['password'].encode('utf-8'))
    else: 
        return None

#Create a User
@router.post("/signup",response_description="User Added Successfully to database")
async def CreateNewUser(user:UserCreateSchema=Body(...)):

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

#Login a user
@router.post("/login",response_description="User Successfully Logged In")
async def LoginUser(user:UserLoginSchema=Body(...)):

    if await CheckLogin(user):
        userData= await get_user_by_email(user.emailID)
        return create_jwt_token(userData["id"])
    else:
        return ErrorResponseModel("An Error Occured",404,"Email ID or Password Incorrect")

#Update a user
@router.patch("/update",response_description="User Data Updated Successfully")
async def UpdateUser(token:str=Depends(JWTBearer()),data:UpdateUserSchema=Body(...)):

    userId=decode_jwt(token)

    existing_user=await get_user_by_id(userId["userId"])

    if existing_user:

        updated_user= await update_user(userId=userId["userId"],data=data)
        if updated_user:
            return ResponseModel("User Data Updated Successfully")
        return ErrorResponseModel("An Error Occured",403,"Unable to update User")

    else:
        return ErrorResponseModel("An Error Occured",404,"No User Found")

#Delete a user
@router.delete("/delete",response_description="User Deleted")
async def DeleteUser(token:str=Depends(JWTBearer())):

    userId=decode_jwt(token)

    deleted_user=await delete_user(userId=userId['userId'])
    if deleted_user:
        return ResponseModel("User Deleted")
    return ErrorResponseModel("Internal Server Error",500,"Unable to delete user")