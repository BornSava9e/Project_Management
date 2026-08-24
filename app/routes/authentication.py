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


def fetch_user(q):
    try:
        collection =  db['users']
        data = collection.find_one(q)
        return data
    except Exception as e:
        return e


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
        token_id =  secrets.token_urlsafe(16)
        refresh_token =  secrets.token_urlsafe(32)
        refresh_collection =  db["refresh_tokens"]
        refresh_payload = {
            "user_id" : check_user['_id'],
            "token_id" : token_id,
            "token_hash" : ph.hash(refresh_token),
            "expires_at" : int((datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=7)).timestamp()),
            "created_at": int(datetime.datetime.now(datetime.UTC).timestamp()),
            "revoked" : False,
            "revoked_at" : None
        }

        refresh_collection.insert_one(refresh_payload)
        return {"status" : "ok", "access_token": token, "refresh_token" : f"{token_id}.{refresh_token}"}
    except Exception as e:
        print(f"Internal Server Error: {e}")
        return JSONResponse(
            status_code=500,
            content={
                "status" : "Error",
                "message" : "Internal Server Error!"
            }
        )


@router.post("/logout", response_model=dict)
async def logout(req : Request):
    try:
        body = await req.json()
        print(body)
        refresh_token = body['refreshToken']
        if not refresh_token:
            print(f"Refresh Token is missing!")
            return JSONResponse(
                status_code=400,
                content= {
                    "status" : "Error",
                    "message" : "Please provide refresh Token!"
                }
            )

        parts = refresh_token.split(".")
        if len(parts) != 2:
            return JSONResponse(
                status_code=400,
                content={"status": "Error", "message": "Invalid refresh token format!"}
            )

        token_id, token = parts  

        print(token, token_id)

        refresh_collection =  db['refresh_tokens']
        token_data =  refresh_collection.find_one({"token_id" : token_id, "revoked" : False})

        if not token_data:
            print("No user Found")
            return JSONResponse(
                            status_code=404,
                            content={
                                "status" : "error", 
                                "message" : "user not found!"
                            }
                        )
        check_token =  ph.verify(token_data['token_hash'], token)

        if not check_token:
            print("Incorrect Refresh Token")
            return JSONResponse(
                status_code=400,
                content= {
                    "status": "error",
                    "message" : "Invalid Refresh Token!"
                }
            )

        result =  refresh_collection.update_one({"token_id" : token_id, "revoked" : False},{"$set": {"revoked" : True, "revoked_at" : int(datetime.datetime.now(datetime.UTC).timestamp())}})

        if result.matched_count == 0:
            print('No User found!')
            return JSONResponse(
                status_code=404,
                content={
                    "status" : "error", 
                    "message" : "user not found!"
                }
            )
        return JSONResponse(
            status_code=200,
            content={
                "status" : "success",
                "message" : "user logout successfully!"
            }
        )
    except Exception as e:
        print(f"ERROR: {e}")
        raise HTTPException(
            status_code=500,
            detail= f"Internal Server Error : {e}"
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


@router.post("/refresh")
async def refresh_token(req : Request):
    try:
        token =  req.headers.get("Authorization")
        body = await req.json()   # raw JSON payload
        print(body)
        refresh_token =  body["refreshToken"]
        

        if not refresh_token:
            print('Please Provide Refresh Token!')
            return JSONResponse(
                status_code=400,
                content={
                    "status" : "error",
                    "message" : "Refresh Token is missing in payload!"
                }
            )
        payload_token = refresh_token.split(".")
        payload_token = refresh_token.split(".")
        if len(payload_token) != 2:
            raise ValueError("Invalid token format. Expected 'token_id.secret'")

        refresh_token_collection =  db['refresh_tokens']
        token_id, token = payload_token
        token_data =  refresh_token_collection.find_one({"token_id" : token_id, "revoked" : False, "expires_at" : {"$gt" : int(datetime.datetime.now(datetime.UTC).timestamp())}})

        if not token_data:
            print('Token Not Found!')
            raise HTTPException(
                status_code=404,
                detail= "Token Expired"
            )

        check_token =  ph.verify(token_data['token_hash'], token)
        print(f"Checking the token and verifying it {check_token}")

        if not check_token:
            print("Token verification failed!")

        print(token_data['user_id'])
        fetch_user_detail = fetch_user({"_id" : ObjectId(token_data['user_id'])})
        n_acc_tok =  jwt.encode({
              "sub" : str(fetch_user_detail['_id']),
              "role" : fetch_user_detail['role'],
              "iat": int(datetime.datetime.now(datetime.UTC).timestamp()),
              "exp": int((datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=15)).timestamp())
        },secret.jwt_secret,secret.jwt_algorithm)

        return JSONResponse(
            status_code=200,
            content={
                "status" : "success",
                "token" : n_acc_tok,
                "refesh_token" : refresh_token
            }
        )


    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(
            status_code=500,
            detail= f"Internal Server Error : {e}"
        )