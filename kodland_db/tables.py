from sqlalchemy import Column, Integer, String, TEXT
from .db import Base


class Users(Base):

    __tablename__ = 'avito'

    item = Column(String, unique=True, index=True, primary_key=True)
    price = Column(TEXT)
    city = Column(TEXT)
    region = Column(TEXT)
    link = Column(TEXT)
    
class Search(Base):

    __tablename__ = 'search'

    pages = Column(Integer, primary_key=True)
    text_input = Column(TEXT)
    date = Column(TEXT)