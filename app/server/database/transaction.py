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
    """
    Info: 
        Adds a transaction
    Parameter:
        transaction_data:Transaction which needs to be added
    Return Value:
        The id corresponding to the transaction
    """
    trs=await transaction_collection.insert_one(transaction_data)
    new_trs=await transaction_collection.find_one({"_id":ObjectId(trs.inserted_id)})
    return str(new_trs["_id"])

#Delete a transaction
async def delete_transaction(t_id:str):
    """
    Info: 
        Deletes a transaction
    Parameter:
        t_id: A valid transaction ID
    Return Value:
        True: Success
        False: Failure
    """
    trs = await transaction_collection.find_one({"_id":ObjectId(t_id)})

    if trs:
        await transaction_collection.delete_one({"_id":ObjectId(trs["_id"])})
        return True
    return False

#Delete all transaction
async def delete_all_transaction(u_id:str):
    """
    Info: 
        Deletes all transaction for a user
    Parameter:
        u_id: A valid user ID
    Return Value:
        True: Successful
        False: Failure
    """
    trs_count = transaction_collection.count_documents({"userID":u_id})

    if trs_count > 0:
        await transaction_collection.delete_many({"userID":u_id})
        return True
    return False


#Update a Transaction
async def update_transaction(t_id:str,data:dict)->dict:
    """
    Info: 
        Updates a transaction
    Parameter:
        t_id: A valid transaction ID
        data: Updated transaction
    Return Value:
        The details of the updated transaction
    """
    trs = await transaction_collection.find_one({"_id":ObjectId(t_id)})

    if trs:
        updated_trs= await transaction_collection.update_one({"_id":ObjectId(trs["_id"])},{"$set":data})
        if updated_trs:
            return transaction_helper(updated_trs)
        return False


#Get a transaction
async def get_transaction(t_id:str)->dict:
    """
    Info: 
        Fetches a transaction 
    Parameter:
        t_id: A valid transaction ID
    Return Value:
        The details of the transaction
    """
    trs=await transaction_collection.find_one({"_id":ObjectId(t_id)})

    if trs:
        return transaction_helper(trs)
    else:
        return None

#Get all transaction for a user
async def get_all_transaction(u_id:str)->List[Dict]:
    """
    Info: 
        Fetches all transaction for a User
    Parameter:
        u_id: A Valid User ID
    Return Value:
        A list of transaction for the user
    """
    cursor = transaction_collection.find({"userID":u_id}).sort({"transactionDate":-1})

    trs=[]
    for document in await cursor.to_list():
        trs.append(document)

    if len(trs) >0:
        return trs
    else:
        return None

#Get all Income Transaction for a user
async def get_all_income_transaction(u_id:str)->List[Dict]:
    """
    Info: 
        Fetches all INCOME type transaction for a User
    Parameter:
        u_id: A Valid User ID
    Return Value:
        A list of transaction
    """
    try:
        cursor=transaction_collection.find({"userID":u_id,"transactonType":"INCOME"}).sort({"transactionDate":-1})

        trs=[]
        for document in await cursor.to_list():
            trs.append(document)

        if len(trs)>0:
            return trs
        else:
            return None
    except Exception as e:
        print("get_all_income_transaction failed with Exception:"+e)
        return False

#Get all Expense Transaction for a user
async def get_all_expense_transaction(u_id:str)->List[Dict]:
    """
    Info: 
        Fetches all EXPENSE type transaction for a User
    Parameter:
        u_id: A Valid User ID
    Return Value:
        A list of transaction
    """
    try:
        cursor=transaction_collection.find({"userID":u_id,"transactonType":"EXPENSE"}).sort({"transactionDate":-1})

        trs=[]
        for document in await cursor.to_list():
            trs.append(document)

        if len(trs)>0:
            return trs
        else:
            return None
    except Exception as e:
        print("get_all_expense_transaction failed with Exception:"+e)
        return False


""""
    Below is example of Redundant Code. 
    Violates the DRY Principle. 
    The logic implemented below could be easily achieved by some client side filtering. 
    Implementing the below code as API routes would add unecessary API calls in the Client Side.
    
"""


#Get Transaction by Month
async def get_transaction_by_month(u_id:str,month:str,year:str)->List[Dict]:
    """
    Info: 
        Fetches all transaction for a given month and year for a User
    Parameter:
        u_id: A valid User ID
        month: A valid Month
        year: A valid Year
    Return Value:
        A list of transaction for a given month and year
    """
    try:
        cursor=transaction_collection.find({"userID":u_id,"transactionMonth":month,"transactionYear":year}).sort({"transactionDate":-1})

        trs=[]
        for document in await cursor.to_list():
            trs.append(document)

        if len(trs)>0:
            return trs
        else:
            return None
    except Exception as e:
        print("get_transaction_by_month failed with Exception:"+e)
        return False

#Get Income Transaction by Month
async def get_income_transaction_by_month(u_id:str,month:str,year:str)->List[Dict]:
    """
    Info: 
        Fetches all INCOME type transaction for a given month and year for a User
    Parameter:
        u_id: A valid User ID
        month: A valid Month
        year: A valid Year
    Return Value:
        A list of Income type transaction for a given month and Year
    """
    try:
        cursor=transaction_collection.find({"userID":u_id,"transactionMonth":month,"transactionYear":year,"transactionType":"INCOME"}).sort({"transactionDate":-1})

        trs=[]
        for document in await cursor.to_list():
            trs.append(document)

        if len(trs)>0:
            return trs
        else:
            return None
    except Exception as e:
        print("get_income_transaction_by_month failed with Exception:"+e)
        return False

#Get Expense Transaction by Month
async def get_expense_transaction_by_month(u_id:str,month:str,year:str)->List[Dict]:
    """
    Info: 
        Fetches all Expense type transaction for a given month and year for a User
    Parameter:
        u_id: A valid User ID
        month: A valid Month
        year: A valid Year
    Return Value:
        A list of Expense type transaction for a given month and Year
    """
    try:
        cursor=transaction_collection.find({"userID":u_id,"transactionMonth":month,"transactionYear":year,"transactionType":"EXPENSE"}).sort({"transactionDate":-1})

        trs=[]
        for document in await cursor.to_list():
            trs.append(document)

        if len(trs)>0:
            return trs
        else:
            return None
    except Exception as e:
        print("get_expense_transaction_by_month failed with Exception:"+e)
        return False


#Get Transaction By Year
async def get_transaction_by_year(u_id:str,year:str)->List[Dict]:
    """
    Info: 
        Fetches all transaction for a given year for a User
    Parameter:
        u_id: A valid User ID
        month: A valid Month
        year: A valid Year
    Return Value:
        A list of transaction for a given year
    """
    try:
        cursor=transaction_collection.find({"userID":u_id,"transactionYear":year}).sort({"transactionDate":-1})

        trs=[]
        for document in await cursor.to_list():
            trs.append(document)

        if len(trs)>0:
            return trs
        else:
            return None
    except Exception as e:
        print("get_transaction_by_year failed with Exception:"+e)
        return False

#Get Income Transaction By Year
async def get_income_transaction_by_year(u_id:str,year:str)->List[Dict]:
    """
    Info: 
        Fetches all Income type transaction for a given year for a User
    Parameter:
        u_id: A valid User ID
        month: A valid Month
        year: A valid Year
    Return Value:
        A list of Income transaction for a given year
    """
    try:
        cursor=transaction_collection.find({"userID":u_id,"transactionYear":year,"transactionType":"INCOME"}).sort({"transactionDate":-1})

        trs=[]
        for document in await cursor.to_list():
            trs.append(document)

        if len(trs)>0:
            return trs
        else:
            return None
    except Exception as e:
        print("get_income_transaction_by_year failed with Exception:"+e)
        return False

#Get Expense Transaction By Year
async def get_expense_transaction_by_year(u_id:str,year:str)->List[Dict]:
    """
    Info: 
        Fetches all Expense type transaction for a given year for a User
    Parameter:
        u_id: A valid User ID
        month: A valid Month
        year: A valid Year
    Return Value:
        A list of Expense transaction for a given year
    """
    try:
        cursor=transaction_collection.find({"userID":u_id,"transactionYear":year,"transactionType":"EXPENSE"}).sort({"transactionDate":-1})

        trs=[]
        for document in await cursor.to_list():
            trs.append(document)

        if len(trs)>0:
            return trs
        else:
            return None
    except Exception as e:
        print("get_expense_transaction_by_year failed with Exception:"+e)
        return False

#Get Transaction by date range
async def get_transaction_by_date_range(u_id:str,from_date:date,to_date:date)->List[Dict]:
    pass