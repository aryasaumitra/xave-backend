from decouple import config
import motor.motor_asyncio as moto

# Set Up Database
MONGO_DETAILS=config("MONGO_DETAILS") 

client = moto.AsyncIOMotorClient(MONGO_DETAILS)

database=client.xave
