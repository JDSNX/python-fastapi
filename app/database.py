from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import time
import psycopg2
from psycopg2.extras import RealDictCursor
from .config import settings

SQLALCHEMY_DATABASE_URL=f"postgresql://{settings.db_username}:{settings.db_password}@{settings.db_hostname}:{settings.db_port}/{settings.db_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()

# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', 
#                                 database='fastapi', 
#                                 user='postgres', 
#                                 password='r3db3rr13s', 
#                                 cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print('[INFO]\tConnected to database...')
#         break
#     except Exception as e:
#         print(f'[ERROR] {e}')
#         time.sleep(2)