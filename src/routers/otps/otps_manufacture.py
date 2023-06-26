

import datetime
from operator import or_
import uuid
from fastapi import (
    Depends,
)
from sqlalchemy.orm import Session

from src.models.users.otp_blocks_model import OTPBlocksModel
from src.models.users.otps_model import OTPsModel
from src.utils.otp import random_otp
from src.models.enums.otp import OTPStatusEnum
from src.database import db_session
from src.utils import logger

LOG = logger.get_app_logger()

def save_record_otp(user_id: int, session: Session) -> OTPsModel:
    # create otp code for user to verify
    otp_code = random_otp(6)

    # create session id for user
    session_id = str(uuid.uuid1())

    # create user token
    otps = OTPsModel()
    otps.user_id = user_id
    otps.status = OTPStatusEnum.not_used
    otps.otp_failed_count = 0
    otps.session_id = session_id
    otps.otp_code = otp_code

    # save the record
    session.add(otps)

    # session execute current transaction
    session.commit()
    return otps


def find_otp_lifetime(user_id: int, session_id: str, session: Session):
    since = datetime.datetime.now() - datetime.timedelta(seconds=10)
    query = session.query(OTPsModel).filter(
        OTPsModel.user_id == user_id and OTPsModel.session_id == session_id and or_(
            OTPBlocksModel.created == None,
            OTPBlocksModel.created > since)).first()
    
    return query

def save_otp_failed_count(lifetime_result: OTPsModel, session: Session):
    lifetime_result.otp_failed_count = lifetime_result.otp_failed_count + 1
    session.merge(lifetime_result)
    session.commit()



def save_blocks_otp(lifetime_result: OTPsModel, session: Session):
    otp_blocks = OTPBlocksModel()
    otp_blocks.user_id = lifetime_result.user_id
    session.add(otp_blocks)
    session.commit()


def disable_otp_code(lifetime_result: OTPsModel, session: Session):
    lifetime_result.status = OTPStatusEnum.already_used
    session.merge(lifetime_result)
    session.commit()
