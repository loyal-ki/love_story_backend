from fastapi import (
    APIRouter,
    Depends,
)

from fastapi.security import OAuth2PasswordRequestForm


from sqlalchemy.orm import Session

from src.schema.base_schema import GenericSuccessResponse, SuccessResponse
from src.errors.errors import UserDataConflict
from src.utils.fastapi import json_response
from src.models.users.users_model import UsersModel
from src.schema.requests.user_schema_request import UserCreateRequest, UserUpdateRequest
from src.schema.responses.user_schema_response import UserAccessToken, UserSchemaResponse
from src.database import db_session
from src.routers.auth.auth_manufacture import create_record_token, create_record_user, getCurrentUser, validate_user_and_password_form


# initial api router
router = APIRouter()


@router.post(
    '/user_creation',
    summary='Account creation API',
    response_description='Information about the user account created.',
    operation_id="user_creation_post",
    response_model=GenericSuccessResponse[UserSchemaResponse],
    # responses=get_routers_responses(DataConflictError, InvalidParameterError)
)
def user_create_api(
        request_data: UserCreateRequest,
        session: Session = Depends(db_session)
):
    """
    Account creation API </br>
    Endpoint: /api/auth/user_creation </br>
    --- </br>
    Raises: </br>
        - 409: DataConflictError </br>
        ... </br>
    Returns: </br>
        _type_: _description_
    """

    # Return 409 if there is an account with the same username
    # Since the username becomes the login ID as it is, if there is an account with the same username, it will be duplicated
    current_user = session.query(UsersModel).filter(
        UsersModel.email == request_data.email).first()

    # Check if user record exists
    if current_user is not None:
        raise UserDataConflict(
            description="Email already exist, please login and complete registration!")

    # create user
    new_user = create_record_user(request_data)

    # Save the record
    session.add(new_user)

    # Flush all the object changes to the database
    session.flush()

    # create user token
    tokens = create_record_token(session, new_user)

    # save the record
    session.add(tokens)

    # session execute current transaction
    session.commit()

    # create response
    user_response: UserSchemaResponse = {
        "user_info": {
            "email": new_user.email,
            "first_name": new_user.first_name,
            "last_name": new_user.last_name,
            "age": new_user.age,
            "phone_number": new_user.phone_number,
            "gender": new_user.gender,
            "profile_picture": new_user.profile_picture,
        },
        "user_token": {
            "access_token": tokens.access_token,
            "refresh_token": tokens.refresh_token,
            "expires_in": tokens.expires_in,
            "issued_at": tokens.issued_at,
            "refresh_token_expires_in": tokens.refresh_token_expires_in,
            "token_type": tokens.token_type
        }
    }

    # Return registered user information for the application
    return json_response({
        **SuccessResponse.default(),
        "data": user_response
    })


@router.put(
    '/user_update',
    summary='Account creation API',
    response_description='Information about the user account created.',
    operation_id="user_update_post",
    response_model=GenericSuccessResponse[UserUpdateRequest],
    # responses=get_routers_responses(DataConflictError, InvalidParameterError)
)
def user_create_api(
        request_data: UserUpdateRequest,
        current_user: UsersModel = Depends(getCurrentUser),
        session: Session = Depends(db_session)
):
    """
    User Update API </br>
    Endpoint: /api/auth/user_update </br>
    --- </br>
    Raises: </br>
        - 400: InvalidParameterError </br>
        ... </br>
    Returns: </br>
        _type_: _description_
    """

    # Return registered user information for the application
    return json_response({
        **SuccessResponse.default(),
    })


@router.post(
    '/user_token',
    summary='Access token issuing API (OAuth2 compliant)',
    response_description='A JWT-encoded access token.',
    operation_id="user_token_post",
    response_model=GenericSuccessResponse[UserAccessToken],
)
def user_token_api(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(db_session)
):
    """
    User Complete Registration API </br>
    Endpoint: /api/auth/user_complete_registration </br>
    --- </br>
    Raises: </br>
        - 400: InvalidParameterError </br>
        ... </br>
    Returns: </br>
        _type_: _description_
    """
    current_user = validate_user_and_password_form(
        form_data.username, form_data.password)

    # create user token
    tokens = create_record_token(session, current_user)

    # save the record
    session.add(tokens)

    data_response: UserSchemaResponse = {
        "access_token": tokens.access_token,
        "refresh_token": tokens.refresh_token,
        "token_type": tokens.token_type
    }

    # Return registered user information for the application
    return json_response({
        **SuccessResponse.default(),
        "data": data_response
    })
