from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    # mongo_url is the field your app will use.
    # Field(..., alias="MONGO_URI") tells Pydantic:
    #   - Look for an environment variable named MONGO_URI
    #   - Assign its value to mongo_url
    mongo_url: str = Field(..., alias="MONGO_URI")
    jwt_secret: str = Field(..., alias="JWT_SECRET")
    jwt_algorithm: str = Field(..., alias="JWT_ALGORITHM")

    class Config:
        # env_file=".env" tells Pydantic to load variables from a local .env file
        env_file = ".env"
        # populate_by_name=True allows you to use mongo_url in code,
        # even though the actual env variable is MONGO_URI
        populate_by_name = True




# from dotenv import load_dotenv
# import os

# load_dotenv()  # loads .env file

# db_url = os.getenv("DATABASE_URL")
# secret = os.getenv("SECRET_KEY")
