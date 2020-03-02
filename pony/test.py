from pony.orm import *
from transactions import *
import os
import time
from random import randint


tran_choice = [newOrder_tran,  payment_tran]#delivery_tran, stockLevel_tran]
db.generate_mapping(create_tables=True)

cnt = 0
start = now = time.time()
while True:
	choice(tran_choice)()
	now = time.time()
	if now - start >= 10:
		start = now
		print(cnt)
		cnt = 0
		continue
	cnt += 1
