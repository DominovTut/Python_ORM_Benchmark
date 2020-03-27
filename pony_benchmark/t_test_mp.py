from pony.orm import *
from transactions import *
import os
import time
from random import randint
from multiprocessing import Process, Value


def test_controler(cnt, run, start, gl_start):
	while run.value:
		now = time.time()
		if now - gl_start >= 61:
			run.value = False
		if now - start.value >= 10:
			print(cnt.value)
			with cnt.get_lock():
				cnt.value = 0
			with start.get_lock():
				start.value = now

		

def test(cnt, run):
	now = time.time()
	while run.value:
		delivery_tran(randint(1, 5))
		with cnt.get_lock():
			cnt.value += 1


db.generate_mapping(create_tables=True)

if __name__ == '__main__':
	cnt = Value('i', 0)
	start = Value('d', 0.0)
	processes = []
	start.value = gl_start = time.time()
	run = Value('b', True)

	for i in range(2):
		process = Process(target=test, args=(cnt, run))
		process.start()
		processes.append(process)
	process = Process(target=test_controler, args=(cnt, run, start, gl_start))
	process.start()
	processes.append(process)


	for process in processes:
		process.join()
