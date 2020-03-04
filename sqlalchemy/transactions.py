from models import *
from random import randint, choice
from datetime import datetime

from models import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

MAX_W_ID = 5
MAX_ITEM_ID = 100
MAX_C_ID = 10




def newOrder_tran(w_id, c_id, i_id):
	Session = sessionmaker(bind=engine)
	session = Session()
	
	whouse = session.query(Warehouse).filter(Warehouse.id == w_id).first()
	districts = session.query(District).filter(District.d_warehouse == whouse.id)
	district = choice(list(districts))
	customer = session.query(Customer).filter(Customer.id == c_id).first()
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
		item = session.query(Item).filter(Item.id == i_id).first()
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
		
		
def payment_tran(w_id, c_id):
	Session = sessionmaker(bind=engine)
	session = Session()
	
	whouse = session.query(Warehouse).filter(Warehouse.id == w_id).first()
	districts = session.query(District).filter(District.d_warehouse == whouse.id)
	district = choice(list(districts))
	customer = session.query(Customer).filter(Customer.id == c_id).first()
	h_amount = randint(10, 5000)
	
	whouse.w_ytd += h_amount
	district.d_ytd += h_amount
	customer.c_balance -= h_amount
	customer.c_ytd_payment += h_amount
	customer.c_payment_cnt += 1
	
	session.add(History(
		h_amount=h_amount,
		h_data='new_paynment',
		h_date=datetime.now(),
		h_customer=customer.id,
	))	
	session.commit()


def orderStatus_tran(c_id):
	Session = sessionmaker(bind=engine)
	session = Session()
	
	customer = session.query(Customer).filter(Customer.id == c_id).first()
	last_order = session.query(Order).filter(Order.o_customer == customer.id).order_by(text("id desc")).first()
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
	



def delivery_tran(w_id):
	Session = sessionmaker(bind=engine)
	session = Session()
	
	whouse = session.query(Warehouse).filter(Warehouse.id == w_id).first()
	districts = session.query(District).filter(District.d_warehouse == whouse.id)
	for district in districts:
		order = session.query(Order).filter(Order.o_district == district.id and Order.is_o_delivered == False).order_by(text("id")).first()
		session.query(Order).filter(Order.o_district == district.id and Order.is_o_delivered == False).order_by(text("id")).first()
		if not order:
			return
		order.is_o_delivered = True
		for o_l in order.o_lns:
			o_l.ol_delivery_d = datetime.now()
		customer = session.query(Customer).filter(Customer.id == order.o_customer).first()
		customer.c_delivery_cnt += 1
	session.commit()


def stockLevel_tran():
	pass