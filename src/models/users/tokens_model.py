from sqlalchemy import (
    Column,
    String,
    Integer,
    BigInteger,
    Boolean,
)

from src.models.base_model import Base


class TokensModel(Base):
    __tablename__ = "tokens"

    id = Column(BigInteger, primary_key=True, autoincrement=True)

    # user id
    user_id = Column(BigInteger, index=True)

    # Token that clients use to make API requests on behalf of the resource owner.
    access_token = Column(String(255))

    # Token used by clients to exchange a refresh token for an access
    # token when the access token has expired.
    refresh_token = Column(String(255))

    # Time date in which token was issued at.
    issued_at = Column(Integer)

    # Time date in which token will expire.
    expires_in = Column(Integer)

    # Time date in which refresh token will expire.
    refresh_token_expires_in = Column(Integer)

    # Type of token expected.
    token_type = Column(String(20))

    # Flag that indicates whether or not the token has been revoked.
    revoked = Column(Boolean)

    def json(self):
        return {
            'access_token': self.access_token,
            'refresh_token': self.refresh_token,
            'issued_at': self.issued_at,
            'expires_in': self.expires_in,
            'refresh_token_expires_in': self.refresh_token_expires_in,
            'token_type': self.token_type,
            'revoked': self.revoked
        }

    FIELDS = {
        'id': int,
        'user_id': int,
        'access_token': str,
        'refresh_token': str,
        'issued_at': int,
        'expires_in': int,
        'refresh_token_expires_in': int,
        'token_type': str,
        'revoked': bool,
    }

    FIELDS.update(Base.FIELDS)
