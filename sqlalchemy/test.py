import os
import time
from random import choice

from models import *
from sqlalchemy.orm import sessionmaker
from transactions import *

tran_choice = [newOrder_tran,  payment_tran, orderStatus_tran]#, delivery_tran, stockLevel_tran]


cnt = 0
start = now = time.time()
while True:
	choice = randint(1, 100)
	if choice <= 45:
		w_id = randint(1, 5)
		c_id = randint(1, 10)
		i_id = randint(1, 100)
		newOrder_tran(w_id, c_id, i_id)
	elif choice <= 88:
		w_id = randint(1, 5)
		c_id = randint(1, 10)
		payment_tran(w_id, c_id)
	elif choice <= 92:
		c_id = randint(1, 10)
		orderStatus_tran(c_id)
	elif choice <= 96:
		delivery_tran()
	else:
		stockLevel_tran()
	now = time.time()
	if now - start >= 10:
		start = now
		print(cnt)
		cnt = 0
		continue
	cnt += 1