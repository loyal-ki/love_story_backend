from datetime import datetime

from sqlalchemy import *
from sqlalchemy.exc import ProgrammingError
from migrate import *
from migrations.log import LOG

meta = MetaData()
table = Table(
    "otp_blocks", meta,
    Column("id", BigInteger, primary_key=True, autoincrement=True),
    Column("user_id", BigInteger, index=True),
    Column("created", DateTime, default=datetime.utcnow),
    Column("modified", DateTime, default=datetime.utcnow,
           onupdate=datetime.utcnow)
)


# Upgrade
def upgrade(migrate_engine):
    meta.bind = migrate_engine
    try:
        table.create()
    # NOTE: print WARNING if TABLE already exists
    except ProgrammingError as err:
        LOG.warning(err.orig)


# Downgrade
def downgrade(migrate_engine):
    meta.bind = migrate_engine
    try:
        table.drop()
    except Exception as err:
        LOG.warning(err)
