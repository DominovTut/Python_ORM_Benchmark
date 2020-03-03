from models import *
from random import randint, choice
from datetime import datetime
from pony.orm import *

MAX_W_ID = 5
MAX_ITEM_ID = 100
MAX_C_ID = 10

@db_session(retry=10)
def newOrder_tran(w_id, c_id, i_id):
	whouse = Warehouse[w_id]
	district = choice(list(select(d for d in District if d.d_warehouse == whouse)))
	customer = Customer[c_id]
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
		item = Item[i_id]
		stock = Stock[whouse, item]
		stock.s_order_cnt += 1
		stock.s_quantity -= amount
		ord_line = OrderLine(
			ol_item=item,
			ol_amount=amount,
			ol_order=order
		)
		
		

	


@db_session(retry=10)
def payment_tran(w_id, c_id):
	whouse = Warehouse[w_id]
	district = choice(list(select(d for d in District if d.d_warehouse == whouse)))
	customer = Customer[c_id]
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
		
	
	


@db_session(retry=10)
def orderStatus_tran(c_id):
	customer = Customer[c_id]
	last_order = customer.c_orders.select().order_by(lambda o: desc(o.id)).first()
	o_ls = [] 
	if not last_order:
		return
	for ol in last_order.o_lns:
		o_ls.append({
			'ol_delivery_d' : ol.ol_delivery_d,
			'ol_item' : ol.ol_item,
			'ol_amount' : ol.ol_amount,
			'ol_order' : ol.ol_order
		})

		

	


@db_session
def delivery_tran():
	pass


@db_session
def stockLevel_tran():
	pass