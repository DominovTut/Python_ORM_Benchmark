from pony.orm import *
from transactions import *
from models import *


db.generate_mapping(create_tables=True)

newOrder_tran()