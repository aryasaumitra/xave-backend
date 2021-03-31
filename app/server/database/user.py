from bson.objectid import ObjectId
from .baseDB import database

#Create a collection
user_collection=database.get_collection("user_collection")

#helper

def user_helper(user)->dict:
    return{
        "id":str(user["_id"]),
        "firstName":user["firstName"],
        "lastName":user["lastName"],
        "emailID":user["emailID"],
        # "dateOfBirth":user["dateOfBirth"],
        "password":user["hashedPassword"]
    }


#create function to write data into collection

#Add a user
async def add_user(user_data:dict)->str:
    user=await user_collection.insert_one(user_data)
    new_user=await user_collection.find_one({"_id":user.inserted_id})
    return str(new_user["_id"])

#Retreive user with matching Email
async def get_user_by_email(email:str)->dict:

    user=await user_collection.find_one({"emailID":email})
    if user:
        return user_helper(user)

#Update user with matching Email
async def update_user_by_email(email:str,data:dict)->dict:

    user=await user_collection.find_one({"emailID":email})
    if user:
        updated_user=await user_collection.update_one({"_id":ObjectId(user["_id"])},{"$set":data})
        if updated_user:
            return True
        return False

#Delete user
async def delete_user(email:str):
    user=await user_collection.find_one({"emailID":email})
    if user:
        await user_collection.delete_one({"_id":ObjectId(user["_id"])})
        return True
    return False



