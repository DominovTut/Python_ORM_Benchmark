import os
import time
from random import randint

from models import *
from sqlalchemy.orm import sessionmaker
from transactions import *
from multiprocessing import Process, Value, Lock
from settings import AMOUNT_OF_PROCESSES, TEST_DURATION, PRINT_INTERVAL


def test_controler(cnt, run, start, gl_start):
    while run.value:
        now = time.time()
        if now - gl_start >= TEST_DURATION:
            run.value = False
        if now - start.value >= PRINT_INTERVAL:
            print(cnt.value)
            with cnt.get_lock():
                cnt.value = 0
            with start.get_lock():
                start.value = now


def test(cnt, run):
    now = time.time()
    while run.value:
        choice = randint(1, 100)
        if choice <= 45:
            tran = [new_order_tran,
                    {'w_id': randint(1, AMOUNT_OF_WAREHOUSES), 'c_id': randint(1, AMOUNT_OF_WAREHOUSES * 10)}]
        elif choice <= 88:
            tran = [payment_tran,
                    {'w_id': randint(1, AMOUNT_OF_WAREHOUSES), 'c_id': randint(1, AMOUNT_OF_WAREHOUSES * 10)}]
        elif choice <= 92:
            tran = [order_status_tran, {'c_id': randint(1, AMOUNT_OF_WAREHOUSES * 10)}]
        elif choice <= 96:
            tran = [delivery_tran, {'w_id': randint(1, AMOUNT_OF_WAREHOUSES)}]
        else:
            tran = [stock_level_tran, {'w_id': randint(1, AMOUNT_OF_WAREHOUSES)}]
        
        if tran[0](**tran[1]):
            with cnt.get_lock():
                cnt.value += 1


if __name__ == '__main__':
    cnt = Value('i', 0)
    start = Value('d', 0.0)
    processes = []
    start.value = gl_start = time.time()
    run = Value('b', True)

    for i in range(AMOUNT_OF_PROCESSES):
        process = Process(target=test, args=(cnt, run))
        process.start()
        processes.append(process)
    process = Process(target=test_controler, args=(cnt, run, start, gl_start))
    process.start()
    processes.append(process)

    for process in processes:
        process.join()
