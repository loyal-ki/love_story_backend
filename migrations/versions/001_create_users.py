from datetime import datetime

from sqlalchemy import *
from sqlalchemy.exc import ProgrammingError
from migrate import *
from migrations.log import LOG

meta = MetaData()
table = Table(
    "users", meta,
    Column("id", BigInteger, primary_key=True, autoincrement=True),
    Column("first_name", String(20)),
    Column("last_name", String(20)),
    Column("email", String(255)),
    Column("password", String(255)),
    Column("phone_number", String(20)),
    Column("profile_picture", String(255)),
    Column("age", Integer),
    Column("gender", Integer),
    Column("user_role", String(20)),
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
