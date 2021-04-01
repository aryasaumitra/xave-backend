from datetime import datetime, timedelta,time
from decouple import config
import jwt
from typing import Dict

JWT_SECRET=config('secret')
JWT_ALGORITHM=config('algorithm')

def token_resposne(token:str):
    return {
        "access_token":token,
        "token_type":"Bearer"
    }

def create_jwt_token(userId:str,expires:timedelta=None)->Dict[str,str]:

    if expires:
        expire=datetime.utcnow() + expires
    else:
        expire=datetime.utcnow()+timedelta(days=1)

    payload={
        "userId":userId,
        "expires":expire
    }

    encoded_token=jwt.encode(payload=payload,key=JWT_SECRET,algorithm=JWT_ALGORITHM)

    return token_resposne(encoded_token)

def decode_jwt(token:str)->dict:
    try:
        decoded_token=jwt.decode(token,JWT_SECRET,algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token['expires']>=time.time() else None

    except:
        return {}