from datetime import datetime

from sqlalchemy import *
from sqlalchemy.exc import ProgrammingError
from migrate import *
from migrations.log import LOG

meta = MetaData()
table = Table(
    "otps", meta,
    Column("id", BigInteger, primary_key=True, autoincrement=True),
    Column("user_id", BigInteger, index=True),
    Column("session_id", String(100)),
    Column("otp_code", String(6)),
    Column("status", String(1)),
    Column("otp_failed_count", Integer),
    Column("created", DateTime, default=datetime.now),
    Column("modified", DateTime, default=datetime.now,
           onupdate=datetime.now)
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
