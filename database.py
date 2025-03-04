from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


DATABASE = 'sqlite:///./url_base.db'

engine = create_engine(DATABASE, connect_args={'check_same_thread': False})

session = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()
