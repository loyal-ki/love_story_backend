from sqlalchemy import (
    Column,
    Integer,
    BigInteger,
)

from src.models.base_model import Base


class OTPBlocksModel(Base):
    __tablename__ = "otp_blocks"

    id = Column(BigInteger, primary_key=True, autoincrement=True)

    # user id
    user_id = Column(BigInteger, index=True)

    def json(self):
        return {
            'user_id': self.user_id,
            "created": self.created,
        }

    FIELDS = {
        'id': int,
        'user_id': int,
    }

    FIELDS.update(Base.FIELDS)
