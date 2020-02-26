from models import *
from pony.orm import *
from random import choice, randint
from datetime import datetime

@db_session
def populate(n):
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
				w_yid=float(i * i)
		)

		for j in range(5):
			District(
				d_id=d_cnt,
				d_warehouse=w,
				d_name='dist %d %d' %(w.w_number, j),
				d_street_1='d_st %d' %j,
				d_street_2 ='d_st2 %d' %j,
				d_city=w.w_city,
				d_zip='d_zip %d' %j,
				d_tax=float(j),
				d_yid=float(j * j),
			)
			d_cnt +=1

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
			c_payment_cnt=randint(0, 100000),
			c_balance=randint(0, 100000),
			c_ytd_payment=randint(0, 100000),
			c_data1='customer %d' %i,
			c_dtata2='hello %d'  %i,
			c_district=District[randint(1, 5)],
		)
		District[randint(1, 5)].d_costomers.add(c)
	for i in range(100):
		it = Item(
			i_name='item %d' %i,
			i_price=randint(1, 100000),
			i_data='data'
		)
		for j in range(1, n + 1):
			Stock(
				s_w=Warehouse[j],
				s_i=it,
				s_quantity = 100000,
				s_ytd=randint(1, 100000),
				s_order_cnt=0,
				s_remote_cnt=0,
				s_data="data",
			)
		
		
		
def main():
	db.generate_mapping(create_tables=True)
	populate(5)
	
	
if __name__ == '__main__':
	main()
			
		