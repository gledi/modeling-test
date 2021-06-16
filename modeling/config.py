import os

SECRET_KEY = os.getenv("SECRET_KEY", None)

DATABASE_HOST = os.getenv("DATABASE_HOST", "localhost")
DATABASE_PORT = int(os.getenv("DATABASE_PORT", "3306"))
DATABASE_USER = os.getenv("DATABASE_USER", None)
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", None)
DATABASE_DATABASE = os.getenv("DATABASE_DATABASE", None)
DATABASE_CHARSET = os.getenv("DATABASE_CHARSET", "utf8mb4")
