from datetime import datetime

from sqlalchemy import *
from sqlalchemy.exc import ProgrammingError
from migrate import *
from migrations.log import LOG

meta = MetaData()
table = Table(
    "tokens", meta,
    Column("id", BigInteger, primary_key=True, autoincrement=True),
    Column("user_id", BigInteger, index=True),
    Column("access_token", String(255)),
    Column("refresh_token", String(255)),
    Column("issued_at", Integer),
    Column("expires_in", Integer),
    Column("refresh_token_expires_in", Integer),
    Column("token_type", String(20)),
    Column("revoked", Boolean),
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
    except sqlalchemy.exc.ProgrammingError as err:
        LOG.warning(err.orig)


# Downgrade
def downgrade(migrate_engine):
    meta.bind = migrate_engine
    try:
        table.drop()
    except Exception as err:
        LOG.warning(err)
