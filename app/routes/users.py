from fastapi import APIRouter, Depends
from app.database.connection import db
from app.schema.userSchema import GetUser, CreateUser, LoginUser
from typing import List
from datetime import datetime
from argon2 import PasswordHasher
from fastapi.responses import JSONResponse
from app.dependencies.dependencies import verify_token

router = APIRouter(prefix="/users", tags=["users"])

def serialize_doc(doc, key):
    doc[key] = str(doc[key])
    return doc

@router.post("/", response_model=dict)
def create_user(body: CreateUser):
    try:
        email = str(body.email)
        name = str(body.name)

        collection = db['users']
        email_check = collection.find_one({"email": email})

        if email_check:
            return JSONResponse(
                status_code=409,
                content={
                    "status": "error",
                    "message": "Email already exists!"
                }
            )

        ph = PasswordHasher()
        password = ph.hash(body.password)

        user_body = {
            "name": name,
            "email": email,
            "password_hash": password,
            "role": "user",
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "last_login_at": None
        }
        collection.insert_one(user_body)

        return JSONResponse(
            status_code=201,
            content={
                "status": "success",
                "message": "User created successfully",
                "data": {k: user_body[k] for k in ["name", "email", "created_at"]}
            }
        )
    except Exception as e:
        print(e)
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": "Something went wrong!"
            }
        )

@router.get("/", response_model=List[GetUser])
def get_user(auth_user=Depends(verify_token)):
    try:
        collection = db['users']
        users = collection.find()
        serialize_users = [serialize_doc(user, "_id") for user in users]
        return serialize_users
    except Exception as e:
        print(e)
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": "Something went wrong!"
            }
        )
