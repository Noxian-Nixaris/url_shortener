from sqlalchemy import Column, Integer, String

from database import Base


class Url(Base):
    __tablename__ = 'urls_list'

    id = Column(Integer, primary_key=True, index=True)
    full_url = Column(String)
    short_url = Column(String, index=True)