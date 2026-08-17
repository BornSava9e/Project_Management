from fastapi import FastAPI
import uvicorn
from app.database.connection import db
from app.routes import users

app = FastAPI()

app.include_router(users.router, prefix="/api/v1")


@app.get("/")
def root():
        return "Server is running at port 3000!"

if __name__ == "__main__":
    uvicorn.run("main:app", host = "127.0.0.1", port=3000, reload = True)


































# from fastapi import FastAPI
# import uvicorn
# from app.database.database import collection

# app = FastAPI()

# @app.get("/")
# async def root():
#     # Proper projection: exclude _id
#     users_cursor = collection.find({}, {"_id": 0})
#     users = [{"name" : user['name']} for user in users_cursor]  # iterate over cursor
#     return {"message": "Hello world!", "users": users}

# if __name__ == "__main__":
#     uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)
