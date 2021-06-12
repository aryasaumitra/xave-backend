from fastapi import FastAPI
from .routes.user import router as UserRouter
from .routes.transaction import router as TransactionRouter

app=FastAPI(
    title="Xave API",
    debug=True,
    version="0.1.0"
)

app.include_router(UserRouter,tags=["User"],prefix="/user")
app.include_router(TransactionRouter,tags=["Transaction"],prefix="/transaction")

@app.get('/',tags=['Root'])
async def read_root():
    return {
        "status":"Server Running"
    }