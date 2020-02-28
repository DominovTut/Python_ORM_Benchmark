import os
import time
from random import choice

from models import *
from sqlalchemy.orm import sessionmaker
from transactions import *

tran_choice = [newOrder_tran,  payment_tran, orderStatus_tran, delivery_tran, stockLevel_tran]


cnt = 0
start = now = time.time()
while True:
	#choice(tran_choice)()
	newOrder_tran()
	now = time.time()
	if now - start >= 10:
		start = now
		print(cnt)
		cnt = 0
		continue
	cnt += 1