from sqlalchemy import (
    Column,
    String,
    Integer,
    BigInteger
)

from src.models.base_model import Base


class UsersModel(Base):
    __tablename__ = "users"

    # user id
    id = Column(BigInteger, primary_key=True, autoincrement=True)

    # last name
    first_name = Column(String(20))

    # last name
    last_name = Column(String(20))

    # email
    email = Column(String(255))

    # hash password
    password = Column(String(255))

    # phone number
    phone_number = Column(String(20))

    # profile picture
    profile_picture = Column(String(255))

    # age
    age = Column(Integer)

    # gender
    gender = Column(Integer)

    # Can be a user or an administrator
    user_role = Column(String(20))

    def json(self):
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'password': self.password,
            'phone_number': self.phone_number,
            'profile_picture': self.profile_picture,
            'age': self.age,
            'gender': self.gender,
            'user_role': self.user_role,
        }

    FIELDS = {
        'id': int,
        'first_name': str,
        'last_name': str,
        'email': str,
        'password': str,
        'phone_number': str,
        'profile_picture': str,
        'age': int,
        'gender': int,
        'user_role': str,
    }

    FIELDS.update(Base.FIELDS)
