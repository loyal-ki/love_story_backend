import datetime
from operator import or_
import uuid
from fastapi import (
    APIRouter,
    Depends,
)

from sqlalchemy.orm import Session

from fastapi_mail import FastMail, MessageSchema, MessageType
from src.schema.base_schema import GenericSuccessResponse, SuccessResponse
from src.utils.fastapi import json_response
from src.database import db_session
from src.schema.requests.otps_schema_request import CreateOTPsRequest, VerifyOTPsRequest
from src.errors.errors import NotSupportedError, OTPBlockedWithUserId, OTPCodeHasExpired, OTPCodeIsAlreadyUsed
from src.models.users.otp_blocks_model import OTPBlocksModel
from src.schema.responses.otps_schema_response import CreateOTPsResponse
from src.models.users.otps_model import OTPsModel
from src.routers.otps.otps_manufacture import disable_otp_code, find_otp_lifetime, save_blocks_otp, save_otp_failed_count, save_record_otp
from src.models.enums.otp import OTPStatusEnum
from src.utils.mail import get_mail_connection
from src.utils.path import get_path_directory

# initial api router
router = APIRouter()


@router.post(
    '/send',
    summary='Send otp to email recipient',
    response_description='OTP information about registered user accounts via email .',
    operation_id="otp_send_post",
    response_model=GenericSuccessResponse[CreateOTPsResponse],
)
async def otp_send_api(
    request_data: CreateOTPsRequest,
    session: Session = Depends(db_session)
):

    since = datetime.datetime.now() - datetime.timedelta(minutes=5)

    # check block otp
    otp_blocks = session.query(OTPBlocksModel).filter(
        OTPBlocksModel.user_id == request_data.user_id and or_(
            OTPBlocksModel.created == None,
            OTPBlocksModel.created < since)).first()

    print(otp_blocks)

    if otp_blocks:
        raise OTPBlockedWithUserId

    # retrieve data from otp model
    otps = save_record_otp(request_data.user_id, session)

    conf = get_mail_connection()
    file_dir = get_path_directory()
    path = file_dir + "/src/templates/authorizations/verified.html"
    with open(path, "r", encoding='utf-8') as file:
        html = file.read().format(otp_code=otps.otp_code)

    message = MessageSchema(
        subject="Love Story - Verify email!",
        recipients=[request_data.email],
        body=html,
        subtype=MessageType.html)

    fm = FastMail(conf)
    await fm.send_message(message)

    # create response to return
    otp_response: CreateOTPsResponse = {
        "user_id": request_data.user_id,
        "session_id": otps.session_id,
    }

    return json_response({
        **SuccessResponse.default(),
        "data": otp_response
    })


@router.post(
    '/verify',
    summary='Verify otp from recipient',
    response_description='Confirm the account has been successfully registered.',
    operation_id="otp_verify_post",
    response_model=SuccessResponse,

)
def otp_verify_post(
    request_data: VerifyOTPsRequest,
    session: Session = Depends(db_session)
):
    lifetime_result = find_otp_lifetime(
        request_data.user_id, request_data.session_id, session)

    # Check OTP code 6 digit lifetime (expired in 60 second)
    if not lifetime_result:
        raise OTPCodeHasExpired

    # Check OTP code is already used
    if lifetime_result.status == OTPStatusEnum.already_used:
        raise OTPCodeIsAlreadyUsed

    # Check OTP not verified
    if lifetime_result.otp_code != request_data.otp_code:
        # Increment OTP failed count
        save_otp_failed_count(lifetime_result, session)

        # Check if OTP code failed count 5 times
        if lifetime_result.otp_failed_count >= 5:
            save_blocks_otp(lifetime_result, session)
            raise OTPBlockedWithUserId

        raise NotSupportedError()

    # Disable otp code when success verified
    disable_otp_code(lifetime_result, session)

    return json_response({
        **SuccessResponse.default(),
    })
