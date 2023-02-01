import os
from dotenv import load_dotenv
from pathlib import Path

dotenv_path = Path('conf/.env')
load_dotenv(dotenv_path=dotenv_path)

# api title
API_TITLE: str = os.environ.get("API_TITLE")

# docker env
DOCKER_ENV: bool = os.environ.get("IN_DOCKER") or False

# redis host
REDIS_HOST: str = os.environ.get("REDIS_HOST") or "redis://localhost"

# root path
ROOT_PATH: str = os.environ.get("LOVE_STORY_ROOT_PATH")

# database name
DB_NAME: str = os.environ.get("DB_NAME") or "lovestorydb"

# database user
DB_USER: str = os.environ.get("DB_USER") or "loyalki"

# database password
DB_PASSWORD: str = os.environ.get("DB_PASSWORD") or "loyalki"

# database host
DB_HOST: str = os.environ.get("DB_HOST") or "localhost"

# database port
DB_PORT = os.environ.get("DB_PORT") or 5432

# secret key
SECRET_KEY: str = os.environ.get("SECRET_KEY") or ""

# algorithm
ALGORITHM: str = os.environ.get("ALGORITHM") or "HS256"

# access token expire
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get(
    "ACCESS_TOKEN_EXPIRE_MINUTES") or 30)

# secret key
REFRESH_SECRET_KEY: str = os.environ.get("REFRESH_SECRET_KEY") or ""

# access token expire
REFRESH_TOKEN_EXPIRE_MINUTES = int(os.environ.get(
    "REFRESH_TOKEN_EXPIRE_MINUTES") or 30)

# log file name
LOG_FILE_NAME: str = os.environ.get("LOG_FILE") or None

# response validate mode
RESPONSE_VALIDATE_MODE: str = os.environ.get(
    "RESPONSE_VALIDATION_MODE") or True

# database url
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# mail username
MAIL_USERNAME: str = os.environ.get("MAIL_USERNAME") or "default@gmail.com"

# mail password
MAIL_PASSWORD: str = os.environ.get("MAIL_PASSWORD")

# mail from
MAIL_FROM: str = os.environ.get("MAIL_FROM")

# mail port
MAIL_PORT: int = int(os.environ.get("MAIL_PORT") or "587")

# mail server
MAIL_SERVER: str = os.environ.get("MAIL_SERVER") or "smtp.gmail.com"
