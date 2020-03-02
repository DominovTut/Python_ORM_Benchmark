from sqlalchemy.orm import sessionmaker
from models import *
from transactions import orderStatus_tran
Session = sessionmaker(bind=engine)
session = Session()

orderStatus_tran()
