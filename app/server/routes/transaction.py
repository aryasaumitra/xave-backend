import re
from ..helper.helper import getISODate, getMonth, getYear
from ..auth.auth_bearer import JWTBearer
from fastapi import Body,APIRouter,status
from fastapi.encoders import jsonable_encoder
from fastapi.param_functions import Depends
from ..auth.auth_handler import decode_jwt

#Importing Database Functions
from ..database.transaction import (
    add_transaction,
    update_transaction,
    delete_transaction,
    delete_all_transaction,
    get_transaction,
    get_all_transaction,
    get_all_income_transaction,
    get_all_expense_transaction,
)

#Import Response Models
from ..models.base import (
    ResponseModel,
    ErrorResponseModel
)

#Importing Transaction Schema
from ..models.transaction import (
    TransactionInfoSchema,
    TransactionDBSchema,
    TransactionUpdateSchema
)


router= APIRouter()

#Create a transaction
@router.post("/create",response_description="Transaction added Successfully",status_code=status.HTTP_201_CREATED)
async def CreateTransaction(data:TransactionInfoSchema=Body(...),token:str=Depends(JWTBearer())):
    
    userID=decode_jwt(token)


    transactionData=TransactionDBSchema(
        transactionAmount=data.transactionAmount,
        transactionType=data.transactionType,
        transactionGrouping=data.transactionGrouping,
        transactionDate=getISODate(data.transactionDate),
        transactionMonth=getMonth(data.transactionDate),
        transactionYear=getYear(data.transactionDate),
        transactionComment=data.transactionComment,
        userID=userID['userId']
    )

    dbTransaction =jsonable_encoder(transactionData)

    newTransaction = await add_transaction(dbTransaction)

    if newTransaction:
        return ResponseModel(newTransaction,"Transaction Added Successfully")
    return ErrorResponseModel("An Error Occured",status.HTTP_404_NOT_FOUND,"Unable to add transaction")


#Update a Transaction
@router.patch("/update/{transaction_id}",response_description="Transaction Updated Successfully",status_code=status.HTTP_200_OK)
async def EditTransaction(transaction_id:str,data:TransactionUpdateSchema=Body(...),token:str=Depends(JWTBearer())):
    
    updatedTransaction= await update_transaction(transaction_id,data)

    if updatedTransaction:
        return ResponseModel(updatedTransaction,"Transaction Updated Successfully")
    return ErrorResponseModel("An Error Occured",status.HTTP_500_INTERNAL_SERVER_ERROR,"Unable to update")

#Delete a Transaction
@router.delete("/{transaction_id}",response_description="Transaction Deleted")
async def RemoveTransaction(transaction_id:str,token:str=Depends(JWTBearer())):

    deleleTrs= await delete_transaction(transaction_id)

    if deleleTrs:
        return ResponseModel({"Delete:Successfull"},"Transaction Deleted")

    return ErrorResponseModel("An Error Occured",status.HTTP_500_INTERNAL_SERVER_ERROR,"Unable to delete")

#Delete all Transaction
@router.delete("/delete/",response_description="All Transaction Removed")
async def RemoveAllTransaction(token:str=Depends(JWTBearer())):

    userId=decode_jwt(token)

    deleteAllTransaction= await delete_all_transaction(userId['userId'])

    if deleteAllTransaction:
        return ResponseModel({"Status":"Successfull"},"Deleted all Transaction Successfully")
    return ErrorResponseModel("An Error Occured",status.HTTP_404_NOT_FOUND,"Unable to delete")


#Get A Transaction
@router.get("/{transaction_id}")
async def GetTransaction(transaction_id:str,token:str=Depends(JWTBearer())):

    transaction=await get_transaction(t_id=transaction_id)

    if transaction:
        return ResponseModel(transaction,"Success")
    return ErrorResponseModel("An Error Occured",status.HTTP_404_NOT_FOUND,"Unable to Find Transaction")

#Get all Transactions for a User
@router.get("/all")
async def GetAllTransaction(token:str=Depends(JWTBearer())):

    userId=decode_jwt(token)

    transactionList=await get_all_transaction(userId['userId'])

    if transactionList:
        return ResponseModel({"Transactions":transactionList},"Success")
    return ErrorResponseModel("An Error Occured",status.HTTP_500_INTERNAL_SERVER_ERROR,"Unable to Fetch Transactions")

#Get All Income Transaction for a User
@router.get("/income")
async def GetIncomeTransaction(token:str=Depends(JWTBearer())):

    userId=decode_jwt(token)

    incomeTransactionList=await get_all_income_transaction(userId['userId'])

    if incomeTransactionList:
        return ResponseModel({"IncomeTransactionList":incomeTransactionList},"Success")
    return ErrorResponseModel("An Error Occured",status.HTTP_500_INTERNAL_SERVER_ERROR,"Unable to Fetch Income")

#Get All Expense Transaction for a user
@router.get("/expense")
async def GetExpenseTransaction(token:str=Depends(JWTBearer())):

    userId=decode_jwt(token)

    expenseTransactionList=await get_all_expense_transaction(userId['userId'])

    if expenseTransactionList:
        return ResponseModel({"ExpenseTransactionList":expenseTransactionList},"Success")
    return ErrorResponseModel("An Error Occured",status.HTTP_500_INTERNAL_SERVER_ERROR,"Unable to Fetch Income")
