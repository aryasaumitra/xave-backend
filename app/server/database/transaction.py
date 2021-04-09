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
    pass

#Delete a transaction
async def delete_transaction(t_id:str):
    pass

#Delete all transaction
async def delete_all_transaction(u_id:str):
    pass

#Update a Transaction
async def update_transaction(t_id:str)->dict:
    pass

#Get a transaction
async def get_transaction(t_id:str)->dict:
    pass

#Get all transaction for a user
async def get_all_transaction(U_id:str)->List[Dict]:
    pass

#Get Transaction by Month
async def get_transaction_by_month(u_id:str,month:str)->List[Dict]:
    pass

#Get Transaction By Year
async def get_transaction_by_year(u_id:str,year:str)->List[Dict]:
    pass

#Get Transaction by date range
async def get_transaction_by_date_range(u_id:str,from_date:date,to_date:date)->List[Dict]:
    pass