from sqlalchemy import (
    Column,
    Integer,
    BigInteger,
    String
)

from src.models.base_model import Base


class OTPsModel(Base):
    __tablename__ = "otps"

    id = Column(BigInteger, primary_key=True, autoincrement=True)

    # user id
    user_id = Column(BigInteger, index=True)

    # gender
    session_id = Column(String(100))

    # otp code send user to verify
    otp_code = Column(String(6))

    # status of otp
    status = Column(String(1))

    # number of times user entered otp failed
    otp_failed_count = Column(Integer, default=0)

    def json(self):
        return {
            'user_id': self.user_id,
            'session_id': self.session_id,
            'otp_code': self.otp_code,
            'status': self.status,
            'otp_failed_count': self.otp_failed_count,
        }

    FIELDS = {
        'id': int,
        'session_id': String,
        'user_id': int,
        'otp_code': String,
        'otp_failed_count': int,
    }

    FIELDS.update(Base.FIELDS)
