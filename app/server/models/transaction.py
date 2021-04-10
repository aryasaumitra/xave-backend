from typing import Optional
from datetime import date
from pydantic import BaseModel,Field

class TransactionInfoSchema(BaseModel):

    transactionAmount: float=Field(...,gt=0.0)
    transactionType: str=Field(...,)
    transactionGrouping: str=Field(...)
    transactionDate: date=Field(...)
    transactionMonth:str=Field(...)
    transactionYear:str=Field(...)
    transactionComment:str=Field(...)

    class Config:
        schema_extra={
            "example":{
                "transactionAmount":143.0,
                "transactionType":"INCOME",
                "transactionGrouping":"SALARY",
                "transactionDate":"1997-10-22",
                "transactionMonth":"October",
                "transactionYear":"1997",
                "transactionComment":"October Salary"
            }
        }
    

class TransactionDBSchema(TransactionInfoSchema):

    userID: str=Field(...)

    class Config:
        schema_extra={
            "example":{
                "transactionAmount":143.0,
                "transactionType":"INCOME",
                "transactionGrouping":"SALARY",
                "transactionDate":"1997-10-22",
                "transactionMonth":"October",
                "transactionYear":"1997",
                "transactionComment":"October Salary",
                "userID":"12nkl1ndlkn12ioncada"
            }
        }

class TransactionUpdateSchema(BaseModel):

    transactionAmount: Optional[float]=Field(gt=0.0)
    transactionType: Optional[str]
    transactionGrouping: Optional[str]
    transactionDate: Optional[date]
    transactionMonth:Optional[str]
    transactionYear:Optional[str]
    transactionComment:Optional[str]