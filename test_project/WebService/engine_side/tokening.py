import jwt
from datetime import datetime, timedelta
from ws_test import settings

ALGORITHM = 'HS256'
access_token_subject = "access"

def create_token(user_id: int) -> dict:
    access_token_exp = timedelta(minutes=60)
    return {
        "access_token": create_access_token(
            data={
                "user_id": user_id
            },
            expires_delta = access_token_exp
        ),
        "toket_type": "Token"
    }

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire, "sub": access_token_subject})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

token = create_token(4)
print(token)