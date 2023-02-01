from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy.ext.declarative import declarative_base

from src.utils import alchemy


class BaseModel(object):
    created = Column(DateTime, default=datetime.utcnow)
    modified = Column(DateTime, default=datetime.utcnow,
                      onupdate=datetime.utcnow)

    @classmethod
    def find_one(cls, session, id):
        return session.query(cls).filter(cls.get_id() == id).one()

    @classmethod
    def find_update(cls, session, id, args):
        return session.query(cls).filter(cls.get_id() == id).update(args, synchronize_session=False)

    @classmethod
    def get_id():
        pass

    FIELDS = {
        'created': alchemy.datetime_to_timestamp,
        'modified': alchemy.datetime_to_timestamp,
    }


Base = declarative_base(cls=BaseModel)
