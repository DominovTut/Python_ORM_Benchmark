from models import *
from random import randint, choice
from datetime import datetime

from models import *
from sqlalchemy.orm import sessionmaker

MAX_W_ID = 5
MAX_ITEM_ID = 100
MAX_C_ID = 10




def newOrder_tran():
	Session = sessionmaker(bind=engine)
	session = Session()
	
	whouse = session.query(Warehouse).filter(Warehouse.id == randint(1, MAX_W_ID)).first()
	districts = session.query(District).filter(District.d_warehouse == whouse.id)
	district = choice(list(districts))
	customer = session.query(Customer).filter(Customer.id == randint(1, MAX_C_ID)).first()
	ol_cnt = randint(1, 10)
	amount = randint(1, 10)
	
	order = Order(
		o_ol_cnt=ol_cnt,
		o_customer=customer.id,	
		o_entry_d=datetime.now(),
		o_whouse=whouse.id,
		o_district=district.id
	)
	session.add(order)
	session.commit()
	
	
	for i in range(ol_cnt):
		item = session.query(Item).filter(Item.id == randint(1, MAX_ITEM_ID)).first()
		stock = session.query(Stock).filter(Stock.s_w == whouse.id and Stock.s_i == item.id).first()
		stock.s_order_cnt += 1
		stock.s_quantity -= amount
		ord_line = OrderLine(
			ol_item=item.id,
			ol_amount=amount,
			ol_order=order.id,
			ol_delivery_d=datetime.now()
		)
		session.add(ord_line)
	session.commit()
		
		
def payment_tran():
	pass



def orderStatus_tran():
	pass



def delivery_tran():
	pass


def stockLevel_tran():
	pass