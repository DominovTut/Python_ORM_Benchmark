import os
import time
from random import randint

from models import *
from sqlalchemy.orm import sessionmaker
from transactions import *


cnt = 0
start = now = time.time()
while True:
	choice = randint(1, 100)
	if choice <= 45:
		w_id = randint(1, 5)
		c_id = randint(1, 10)
		new_order_tran(w_id, c_id)
	elif choice <= 88:
		w_id = randint(1, 5)
		c_id = randint(1, 10)
		payment_tran(w_id, c_id)
	elif choice <= 92:
		c_id = randint(1, 10)
		order_status_tran(c_id)
	elif choice <= 96:
		w_id = randint(1, 5)
		delivery_tran(w_id)
	else:
		w_id = randint(1, 5)
		stock_level_tran(w_id)
	now = time.time()
	if now - start >= 10:
		start = now
		print(cnt)
		cnt = 0
		continue
	cnt += 1