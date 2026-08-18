import jwt
from fastapi import APIRouter
from app.database.connection import db
from app.schema.userSchema import LoginUser
from fastapi.responses import JSONResponse
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from app.config.settings import Settings
import datetime
router = APIRouter(prefix="/auth/login", tags=['login'])
ph= PasswordHasher()
secret = Settings()


@router.post("/", response_model=dict)
def login(body:LoginUser):
    try:
        print(body)
        collection =  db['users']
        check_user = collection.find_one({"email" : body.email})
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
              "name" :  check_user['name'],
              "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }

        token  = jwt.encode(jwt_payload, secret.jwt_secret, secret.jwt_algorithm )
        print(token)

        return {"status" : "ok", "token": token}
    except Exception as e:
        print(f"Internal Server Error: {e}")
        return JSONResponse(
            status_code=500,
            content={
                "status" : "Error",
                "message" : "Internal Server Error!"
            }
        )