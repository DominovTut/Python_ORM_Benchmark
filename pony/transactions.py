from models import *
from random import randint
from datetime import datetime

MAX_W_ID = 5
MAX_ITEM_ID = 100
MAX_C_ID = 10

@db_session
def newOrder_tran():
	whouse = Warehouse[randint(1, MAX_W_ID)]
	district = District[randint(1, 25)]
	customer = Customer[randint(1, MAX_C_ID)]
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
		item = Item[randint(1, MAX_ITEM_ID)]
		stock = Stock[whouse, item]
		stock.s_order_cnt += 1
		stock.s_quantity -= amount
		ord_line = OrderLine(
			ol_item=item,
			ol_amount=amount,
			ol_order=order,
			ol_delivery_d=datetime.now()
		)
		
		

	


@db_session
def payment_tran():
	pass


@db_session
def orderStatus_tran():
	pass


@db_session
def delivery_tran():
	pass


@db_session
def stockLevel_tran():
	pass