import os
from typing import TypedDict

from dotenv import load_dotenv

load_dotenv()


class DBConfig(TypedDict):
    dbname: str
    user: str
    password: str
    host: str
    port: str


DB_PARAMS: DBConfig = {
    "dbname": os.getenv("DB_NAME", ""),
    "user": os.getenv("DB_USER", ""),
    "password": os.getenv("DB_PASSWORD", ""),
    "host": os.getenv("DB_HOST", ""),
    "port": os.getenv("DB_PORT", ""),
}
