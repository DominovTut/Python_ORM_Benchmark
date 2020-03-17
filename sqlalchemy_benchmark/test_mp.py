import os
import time
from random import randint

from models import *
from sqlalchemy.orm import sessionmaker
from transactions import *
from threading import Thread, Lock


CNT = 0
RES = []
lock = Lock()


def test():
	global CNT, start, now, gl_start
	
	while now - gl_start < 60:
		CNT += 1
		choice = randint(1, 100)
		if choice <= 45:
			tran = [new_order_tran, {'w_id' : randint(1, 5), 'c_id' : randint(1, 10)}]
		elif choice <= 88:
			tran = [payment_tran, {'w_id' : randint(1, 5), 'c_id' : randint(1, 10)}]
		elif choice <= 92:
			tran = [order_status_tran, {'c_id' : randint(1, 10)}]
		elif choice <= 96:
			tran = [delivery_tran, {'w_id' : randint(1, 5)}]
		else:
			tran = [stock_level_tran, {'w_id' : randint(1, 5)}]
		for i in range(10):
			try:
				tran[0](**tran[1])
				break
			except:
				continue
		now = time.time()
		if now - start >= 10:
			with lock:
				print(CNT)
				CNT = 0
			start = now



		
gl_start = start = now = time.time()

t1 = Thread(target=test)
t2 = Thread(target=test)
t3 = Thread(target=test)


t1.start()
t2.start()
t3.start()
#counter.start()

t1.join()
t2.join()
t3.join()
			
