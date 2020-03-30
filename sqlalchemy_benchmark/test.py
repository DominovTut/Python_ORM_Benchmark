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
        tran = [new_order_tran, {'w_id' : randint(1, 5), 'c_id' : randint(1, 10)}]
    elif choice <= 88:
        tran = [payment_tran, {'w_id' : randint(1, 5), 'c_id' : randint(1, 10)}]
    elif choice <= 92:
        tran = [order_status_tran, {'c_id' : randint(1, 10)}]
    elif choice <= 96:
        tran = [delivery_tran, {'w_id' : randint(1, 5)}]
    else:
        tran = [stock_level_tran, {'w_id' : randint(1, 5)}]
    
    tran[0](**tran[1])

    now = time.time()
    if now - start >= 10:
        start = now
        print(cnt)
        cnt = 0
        continue
    cnt += 1