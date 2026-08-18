from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from app.config.settings import Settings
import jwt

security = HTTPBearer()
settings = Settings()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload =  jwt.decode(credentials.credentials, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        return payload
    except jwt.ExpiredSignatureError:
        return JSONResponse(
            status_code=401,
            content={
                "status" : "error",
                "message" : "Tokent Expired"
            }
        )