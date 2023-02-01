from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.config.config import DATABASE_URL


# get engine
def get_engine(uri):
    options = {
        'pool_recycle': 3600,
        'pool_size': 10,
        'pool_timeout': 30,
        'pool_pre_ping': True,
        'max_overflow': 30,
        'echo': False
    }
    return create_engine(uri, **options)


# database url
engine = get_engine(DATABASE_URL)

# Session will use for connection
SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)


# create database session
def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
