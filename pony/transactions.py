from models import *
from random import randint, choice
from datetime import datetime
from pony.orm import *

MAX_W_ID = 5
MAX_ITEM_ID = 100
MAX_C_ID = 10

@db_session
def newOrder_tran():
	whouse = Warehouse.select_random(1)[0]
	district = choice(list(select(d for d in District if d.d_warehouse == whouse)))
	customer = Customer.select_random(1)[0]
	ol_cnt = randint(1, 10)
	amount = randint(1, 10)
	
	order = Order(
		o_ol_cnt=ol_cnt,
		o_customer=customer,
		o_entry_d=datetime.now(),
		o_whouse=whouse,
		o_district=district
	)
	
	
	for i in range(ol_cnt):
		item = Item.select_random(1)[0]
		stock = Stock[whouse, item]
		stock.s_order_cnt += 1
		stock.s_quantity -= amount
		ord_line = OrderLine(
			ol_item=item,
			ol_amount=amount,
			ol_order=order
		)
		
		

	


@db_session
def payment_tran():
	whouse = Warehouse.select_random(1)[0]
	district = choice(list(select(d for d in District if d.d_warehouse == whouse)))
	customer = Customer.select_random(1)[0]
	h_amount = randint(10, 5000)
	
	whouse.w_ytd += h_amount
	district.d_ytd += h_amount
	customer.c_balance -= h_amount
	customer.c_ytd_payment += h_amount
	customer.c_payment_cnt += 1
	
	History(
		h_date=datetime.now(),
		h_amount=h_amount,
		h_data='new_paynment',
		h_customer=customer,
	)	
		
	
	


@db_session
def orderStatus_tran():
	customer = Customer.select_random(1)[0]
	last_order = list(select(o for o in Order))[-1]
	ol_s = list(select(ol for ol in OrderLine if ol.ol_order == last_order))

	


@db_session
def delivery_tran():
	pass


@db_session
def stockLevel_tran():
	pass