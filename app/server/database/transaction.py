from bson.objectid import ObjectId
from .baseDB import database

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