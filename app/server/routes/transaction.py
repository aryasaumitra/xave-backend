from ..helper.helper import getISODate, getMonth, getYear
from ..auth.auth_bearer import JWTBearer
from fastapi import Body,APIRouter
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
    get_transaction_by_month,
    get_income_transaction_by_month,
    get_expense_transaction_by_month,
    get_transaction_by_year,
    get_expense_transaction_by_year,
    get_income_transaction_by_year
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
@router.post("/create",response_description="Transaction added Successfully")
async def create_transaction(data:TransactionInfoSchema=Body(...),token:str=Depends(JWTBearer())):
    
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
    return ErrorResponseModel("An Error Occured",)