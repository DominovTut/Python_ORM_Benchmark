from models import *
from random import randint, choice
from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, SmallInteger, String, create_engine, ForeignKey, BigInteger, Float, Boolean, Text 
from sqlalchemy.type import Decimal
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from models import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

from transactions import delivery_tran

class District(Base):
	__tablename__ = 'district'
	
	id = Column(Integer, primary_key=True)
