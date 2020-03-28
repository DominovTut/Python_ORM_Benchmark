from pony.orm import *
from transactions import *
import os
import time
from random import randint
from multiprocessing import Process, Value
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

		

def test(cnt, run, itr):
    now = time.time()
    while run.value:
        if itr == 0:
            tran = [new_order_tran, {'w_id' : randint(1, 5), 'c_id' : randint(1, 10)}]
        elif itr == 1:
            tran = [payment_tran, {'w_id' : randint(1, 5), 'c_id' : randint(1, 10)}]
        elif itr == 2:
            tran = [order_status_tran, {'c_id' : randint(1, 10)}]
		elif itr == 3:
            tran = [delivery_tran, {'w_id' : randint(1, 5)}]
        elif itr == 4:
            tran = [stock_level_tran, {'w_id' : randint(1, 5)}]
        else:
            print("Sonething went wrong")
            return
		
        tran[0](**tran[1])
        with cnt.get_lock():
            cnt.value += 1


db.generate_mapping(create_tables=True)
transactions = (new_order_tran, payment_tran, order_status_tran, delivery_tran, stock_level_tran)

if __name__ == '__main__':
    for itr in range(len(transactions)):
        print('>>>', transactions[itr])
        cnt = Value('i', 0)
        start = Value('d', 0.0)
        processes = []
        start.value = gl_start = time.time()
        run = Value('b', True)

        for i in range(AMOUNT_OF_PROCESSES):
            process = Process(target=test, args=(cnt, run, itr))
            process.start()
            processes.append(process)
        process = Process(target=test_controler, args=(cnt, run, start, gl_start))
        process.start()
        processes.append(process)


        for process in processes:
            process.join()