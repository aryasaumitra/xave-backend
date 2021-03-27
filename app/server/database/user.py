from bson.objectid import ObjectId
from .baseDB import database

#Create a collection
user_collection=database.get_collection("user_collection")

#helper

def user_helper(user)->dict:
    return{
        "firstName":user["firstName"],
        "lastName":user["lastName"],
        "emailID":user["emailID"],
        "dateOfBirth":user["dateOfBirth"]
    }


#create function to write data into collection
