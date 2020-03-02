import os
import time
from random import choice, randint
from datetime import datetime

from models import *
from sqlalchemy.orm import sessionmaker


def populate(n):
	Session = sessionmaker(bind=engine)
	session = Session()

	citys = ('Moscow', 'St. Petersbrg', 'Pshkin', 'Oraneinbaum', 'Vladivostok')
	names = ('Ivan', 'Evgeniy', 'Alexander', 'Fedor', 'Julia', 'Stephany', 'Sergey', 'Natalya', 'Keanu', 'Jhon', 'Harry', 'James' )
	last_names = ('Petrov', 'Ivanov', 'Andreev', 'Mils', 'Smith', 'Anderson', 'Dominov', 'Tishenko', 'Zhitnikov')
	d_cnt = 0
	for i in range(1, n + 1):
		w = Warehouse(
				w_number=i,
				w_street_1='w_st %d' %i,
				w_street_2='w_st2 %d' %i,
				w_city=choice(citys),
				w_zip='w_zip %d' %i,
				w_tax=float(i),
				w_ytd=0
		)
		session.add(w)

		for j in range(5):
			d = District(
				d_warehouse=i,
				d_name='dist %d %d' %(w.w_number, j),
				d_street_1='d_st %d' %j,
				d_street_2 ='d_st2 %d' %j,
				d_city=w.w_city,
				d_zip='d_zip %d' %j,
				d_tax=float(j),
				d_ytd=0,
			)
			session.add(d)
			d_cnt += 1


	for i in range(2 * n):
		c = Customer(
			c_first_name=choice(names),
			c_middle_name=choice(names),
			c_last_name=choice(last_names),
			c_street_1='c_st %d' %i,
			c_street_2='c_st2 %d' %i,
			c_city=choice(citys),
			c_zip='c_zip %d' %i,
			c_phone='phone',
			c_since=datetime(2005, 7, 14, 12, 30),
			c_credit='credit',
			c_credit_lim=randint(1000, 100000),
			c_discount=choice((0, 10, 15, 20, 30)),
			c_delivery_cnt=0,
			c_payment_cnt=0,
			c_balance=1000000,
			c_ytd_payment=0,
			c_data1='customer %d' %i,
			c_dtata2='hello %d'  %i,
			c_district=randint(1, d_cnt),
		)
		session.add(c)
		d = session.query(District).filter(District.id == randint(1, d_cnt)).first()
		d.d_costomers.append(c)
		session.commit()
	for i in range(100):
		it = Item(
			i_name='item %d' %i,
			i_price=randint(1, 100000),
			i_data='data'
		)
		session.add(it)
		for j in range(1, n + 1):
			s = Stock(
				s_w=j,
				s_i=i,
				s_quantity = 100000,
				s_ytd=randint(1, 100000),
				s_order_cnt=0,
				s_remote_cnt=0,
				s_data="data",
			)
			session.add(s)
	session.commit()


if __name__ == '__main__':
	create_tables()
	populate(5)