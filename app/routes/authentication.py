import jwt
from fastapi import APIRouter, Depends, HTTPException, status, Request
from app.database.connection import db
from app.schema.userSchema import LoginUser
from fastapi.responses import JSONResponse
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from app.config.settings import Settings
import datetime
from app.dependencies.dependencies import verify_token
from bson import ObjectId
import secrets

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter(prefix="/auth", tags=['login'])
ph= PasswordHasher()
secret = Settings()


@router.post("/login", response_model=dict)
def login(body:LoginUser):
    try:
        print(body)
        user_collection =  db['users']
        check_user = user_collection.find_one({"email" : body.email})
        print(check_user)
        if not check_user:
            print("user not found")
            return JSONResponse(
                status_code=404,
                content = {
                    "status" : "Not Found",
                    "message" : "User Not found!"
                }
            )
        
        # Password verification must be wrapped in try/except
        try:
            ph.verify(check_user["password_hash"], body.password)
        except VerifyMismatchError:
            print(f"Incorrect Password")
            return JSONResponse(
                status_code=401,
                content={"status": "error", "message": "Incorrect Password!"}
            )
        

        jwt_payload =  {
              "sub" : str(check_user['_id']),
              "role" : check_user['role'],
              "iat": int(datetime.datetime.now(datetime.UTC).timestamp()),
              "exp": int((datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=15)).timestamp())
        }

        token  = jwt.encode(jwt_payload, secret.jwt_secret, secret.jwt_algorithm )
        print(token)
        refresh_token =  secrets.token_urlsafe(32)
        refresh_collection =  db["refresh_tokens"]
        refresh_payload = {
            "user_id" : check_user['_id'],
            "token_hash" : ph.hash(refresh_token),
            "expires_at" : int((datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=7)).timestamp()),
            "created_at": int(datetime.datetime.now(datetime.UTC).timestamp()),
            "revoked" : False,
            "revoked_at" : None
        }

        refresh_collection.insert_one(refresh_payload)
        return {"status" : "ok", "access_token": token, "refresh_token" : refresh_token}
    except Exception as e:
        print(f"Internal Server Error: {e}")
        return JSONResponse(
            status_code=500,
            content={
                "status" : "Error",
                "message" : "Internal Server Error!"
            }
        )


@router.get("/me", response_model=dict)
def auth_me(auth=Depends(verify_token)):
    try:
        user = auth  # decoded JWT payload
        print(user)
        collection = db['users']
        check_user = collection.find_one({"_id": ObjectId(user["sub"])})
        if check_user:
            check_user['_id'] = str(check_user["_id"])
        return {
            "status": "success",
            "data": check_user
        }
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error!"
        )


security = HTTPBearer()
@router.get("/refresh")
def refresh_token(req : Request):
    try:
        token =  req.headers.get("Authorization")
        print(token.replace("Bearer ", ""))
    except Exception as e:
        print(f"Error: {e}")