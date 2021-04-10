from typing import Dict, List
from bson.objectid import ObjectId
from .baseDB import database
from datetime import date

#Create/Get a collection
transaction_collection=database.get_collection('transaction_collection')

#helper
def transaction_helper(transaction)->dict:
    return{
        "id":str(transaction["_id"]),
        "transactionAmount":transaction["transactionAmount"],
        "transactionType":transaction["transactionType"],
        "transactionGrouping":transaction["transactionGrouping"],
        "transactionDate":transaction["transactionDate"],
        "transactionMonth":transaction["transactionMonth"],
        "transactionYear":transaction["transactionYear"],
        "transactionComment":transaction["transactionComment"]
    }

#Functions to write data to collection

#Add a transaction
async def add_transaction(transaction_data:dict)->str:
    trs=await transaction_collection.insert_one(transaction_data)
    new_trs=await transaction_collection.find_one({"_id":ObjectId(trs.inserted_id)})
    return str(new_trs["_id"])

#Delete a transaction
async def delete_transaction(t_id:str):
    trs = await transaction_collection.find_one({"_id":ObjectId(t_id)})

    if trs:
        await transaction_collection.delete_one({"_id":ObjectId(trs["_id"])})
        return True
    return False

#Delete all transaction
async def delete_all_transaction(u_id:str):
    trs_count = transaction_collection.count_documents({"userID":u_id})

    if trs_count > 0:
        await transaction_collection.delete_many({"userID":u_id})
        return True
    return False


#Update a Transaction
async def update_transaction(t_id:str,data:dict)->dict:

    trs = await transaction_collection.find_one({"_id":ObjectId(t_id)})

    if trs:
        updated_trs= await transaction_collection.update_one({"_id":ObjectId(trs["_id"])},{"$set":data})
        if updated_trs:
            return True
        return False


#Get a transaction
async def get_transaction(t_id:str)->dict:
    trs=await transaction_collection.find_one({"_id":ObjectId(t_id)})

    if trs:
        return transaction_helper(trs)
    else:
        return None

#Get all transaction for a user
async def get_all_transaction(u_id:str)->List[Dict]:
    cursor = transaction_collection.find({"userID":u_id}).sort({"transactionDate":-1})

    trs=[]
    for document in await cursor.to_list():
        trs.append(document)

    if len(trs) >0:
        return trs
    else:
        return None


#Get Transaction by Month
async def get_transaction_by_month(u_id:str,month:str,year:str)->List[Dict]:
    pass

#Get Transaction By Year
async def get_transaction_by_year(u_id:str,year:str)->List[Dict]:
    pass

#Get Transaction by date range
async def get_transaction_by_date_range(u_id:str,from_date:date,to_date:date)->List[Dict]:
    pass