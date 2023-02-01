import json
from datetime import datetime, timedelta

from jose import jwt
from jose import JWTError

from passlib.context import CryptContext

from sqlalchemy.orm import Session

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from src.models.users.users_model import UsersModel
from src.models.users.tokens_model import TokensModel
from src.models.enums.gender import GenderEnum
from src.schema.requests.user_schema_request import UserCreateRequest, UserUpdateRequest
from src.config.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, REFRESH_SECRET_KEY, REFRESH_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from src.constants.constants import API_PREFIX, TOKEN_TYPE
from src.errors.errors import UnauthorizedError
from src.utils import logger
from src.database import db_session

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

LOG = logger.get_app_logger()


# create record token
def create_record_token(session: Session, new_user: UsersModel) -> TokensModel:
    LOG.info(new_user)
    # create token model
    tokens = TokensModel()
    tokens.user_id = new_user.id
    tokens.access_token = create_access_token(user_id=new_user.id)
    tokens.refresh_token = create_refresh_token(user_id=new_user.id)
    tokens.expires_in = ACCESS_TOKEN_EXPIRE_MINUTES * 60
    tokens.issued_at = ACCESS_TOKEN_EXPIRE_MINUTES * 60
    tokens.refresh_token_expires_in = REFRESH_TOKEN_EXPIRE_MINUTES * 60
    tokens.token_type = TOKEN_TYPE
    return tokens


# create or update user information
def create_record_user(request_data: UserCreateRequest) -> UsersModel:
    LOG.info(new_user)
    # create user
    new_user = UsersModel()
    new_user.email = request_data.email
    new_user.password = request_data.password
    # hashed password
    new_user.password = get_hashed_password(request_data.password)
    # age default 20
    new_user.age = 20
    new_user.first_name = ""
    new_user.last_name = ""
    new_user.phone_number = ""
    new_user.gender = GenderEnum.male
    new_user.user_role = ""
    new_user.profile_picture = ""
    return new_user


# update record user
def update_record_user(request_data: UserUpdateRequest):
    LOG.info(request_data)
    update_user = UsersModel()
    update_user.age = request_data.age
    update_user.first_name = request_data.first_name
    update_user.last_name = request_data.last_name
    update_user.phone_number = request_data.phone_number
    update_user.gender = request_data.gender
    update_user.user_role = request_data.user_role
    update_user.profile_picture = request_data.profile_picture


# hashed password
def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


# verify password
def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


# create access token
def create_access_token(user_id: str, expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    jwt_payload = {"exp": expires_delta,
                   "sub": json.dumps({'user_id': user_id})}

    access_token = jwt.encode(jwt_payload, SECRET_KEY, ALGORITHM)
    return access_token


# create refresh token
def create_refresh_token(user_id: str, expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)

    jwt_payload = {"exp": expires_delta,
                   "sub": json.dumps({'user_id': user_id})}

    refresh_token = jwt.encode(jwt_payload, REFRESH_SECRET_KEY, ALGORITHM)
    return refresh_token


# get currentUser
async def getCurrentUser(
        token: str = Depends(OAuth2PasswordBearer(
            tokenUrl=f'{API_PREFIX}/token')),
        session: Session = Depends(db_session)) -> UsersModel:
    """
    Get the currently logged in user. It is assumed to be used in Depends() of FastAPI </br>
    An exception is thrown if the Bearer token is not specified, the JWT token is invalid,
    or the user account does not exist. </br>

    Args: </br>
        token (str, optional): _description_. Defaults to Depends(OAuth2PasswordBearer(tokenUrl='users/token')). </br>

    Returns: </br>
        User: User information.
    """

    try:
        # Decode the JWT token
        jwt_payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # User ID is not included in JWT (JWT token is invalid)
        if jwt_payload.get('sub') is None:
            LOG.error("Access token is invalid")
            raise UnauthorizedError

        user_id: str = json.loads(jwt_payload.get('sub', {}))['user_id']

    # invalid JWT token
    except JWTError:
        LOG.error("Access token is invalid")
        raise UnauthorizedError

    current_user_data = session.query(UsersModel).filter(
        UsersModel.id == user_id).first()

    if not current_user_data:
        LOG.error(
            "f'User associated with access token does not exist [user_id: {user_id}]'")
        raise UnauthorizedError

    LOG.info(current_user_data)
    return current_user_data


# Validate a given username and password and issue a JWT-encoded access token for that user.
def validate_user_and_password_form(username: str, password: str, session: Session = Depends(db_session)) -> UsersModel:
    current_user_data = session.query(UsersModel).filter(
        UsersModel.email == username).first()

    if not current_user_data:
        LOG.error(
            f'Incorrect username [username: {username}]')
        raise UnauthorizedError

    if not verify_password(password, current_user_data.password):
        LOG.error(
            f'Incorrect password [username: {username}]')
        raise UnauthorizedError

    return current_user_data
