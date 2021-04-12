from fastapi import FastAPI
from .routes.user import router as UserRouter
from .routes.transaction import router as TransactionRouter

app=FastAPI()

app.include_router(UserRouter,tags=["User"],prefix="/user")
app.include_router(TransactionRouter,tags=["Transaction"],prefix="/transaction")

@app.get('/',tags=['Root'])
async def read_root():
    return {
        "status":"Server Running"
    }