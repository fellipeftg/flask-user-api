import os
from dotenv import load_dotenv

# força carregar o arquivo .env
load_dotenv(".env")


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False