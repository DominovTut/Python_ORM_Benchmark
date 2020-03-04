from pony.orm import *
from transactions import *
import os
import time
from random import randint


db.generate_mapping(create_tables=True)

cnt = 0
start = now = time.time()
while True:
	choice = randint(1, 100)
	if choice <= 45:
		w_id = randint(1, 5)
		c_id = randint(1, 50)
		i_id = randint(1, 100)
		newOrder_tran(w_id, c_id)
	elif choice <= 88:
		w_id = randint(1, 5)
		c_id = randint(1, 50)
		payment_tran(w_id, c_id)
	elif choice <= 92:
		c_id = randint(1, 50)
		orderStatus_tran(c_id)
	elif choice <= 96:
		w_id = randint(1, 5)
		delivery_tran(w_id)
	else:
		w_id = randint(1, 5)
		stockLevel_tran(w_id)
		
	now = time.time()
	if now - start >= 10:
		start = now
		print(cnt)
		cnt = 0
		continue
	cnt += 1
