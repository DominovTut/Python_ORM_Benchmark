from models import *
from random import randint, choice
from datetime import datetime

from models import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

MAX_W_ID = 5
MAX_ITEM_ID = 100
MAX_C_ID = 10




def new_order_tran(w_id, c_id):
	Session = sessionmaker(bind=engine)
	session = Session()
	
	whouse = session.query(Warehouse).filter(Warehouse.id == w_id).first()
	districts = session.query(District).filter(District.warehouse == whouse.id)
	district = choice(list(districts))
	customer = session.query(Customer).filter(Customer.id == c_id).first()
	ol_cnt = randint(1, 10)
	amount = randint(1, 10)
	
	order = Order(
		ol_cnt=ol_cnt,
		customer=customer.id,	
		entry_d=datetime.now(),
		whouse=whouse.id,
		district=district.id
	)
	session.add(order)
	session.commit()
	
	
	for i in range(ol_cnt):
		item = session.query(Item).filter(Item.id == randint(1, 100)).first()
		stock = session.query(Stock).filter(Stock.warehouse == whouse.id and Stock.item == item.id).first()
		stock.order_cnt += 1
		stock.quantity -= amount
		ord_line = OrderLine(
			item=item.id,
			amount=amount,
			order=order.id
		)
		session.add(ord_line)
		session.commit()
		
		
def payment_tran(w_id, c_id):
	Session = sessionmaker(bind=engine)
	session = Session()
	
	whouse = session.query(Warehouse).filter(Warehouse.id == w_id).first()
	districts = session.query(District).filter(District.warehouse == whouse.id)
	district = choice(list(districts))
	customer = session.query(Customer).filter(Customer.id == c_id).first()
	h_amount = randint(10, 5000)
	
	whouse.ytd += h_amount
	district.ytd += h_amount
	customer.balance -= h_amount
	customer.ytd_payment += h_amount
	customer.payment_cnt += 1
	
	session.add(History(
		amount=h_amount,
		data='new_paynment',
		date=datetime.now(),
		customer=customer.id,
	))	
	session.commit()


def order_status_tran(c_id):
	Session = sessionmaker(bind=engine)
	session = Session()
	
	customer = session.query(Customer).filter(Customer.id == c_id).first()
	last_order = session.query(Order).filter(Order.customer == customer.id).order_by(text("id desc")).first()
	o_ls = []
	
	if not last_order:
		return
	for ol in last_order.o_lns:
		o_ls.append({
			'ol_delivery_d' : ol.delivery_d,
			'ol_item' : ol.item,
			'ol_amount' : ol.amount,
			'ol_order' : ol.order
		})
	



def delivery_tran(w_id):
	Session = sessionmaker(bind=engine)
	session = Session()
	
	whouse = session.query(Warehouse).filter(Warehouse.id == w_id).first()
	districts = session.query(District).filter(District.warehouse == whouse.id)
	for district in districts:
		order = session.query(Order).filter(Order.district == district.id and Order.is_o_delivered == False).order_by(text("id")).first()
		session.query(Order).filter(Order.district == district.id and Order.is_o_delivered == False).order_by(text("id")).first()
		if not order:
			return
		order.is_o_delivered = True
		for o_l in order.o_lns:
			o_l.delivery_d = datetime.now()
		customer = session.query(Customer).filter(Customer.id == order.customer).first()
		customer.delivery_cnt += 1
	session.commit()


def stock_level_tran(w_id):
	Session = sessionmaker(bind=engine)
	session = Session()
	
	whouse = session.query(Warehouse).filter(Warehouse.id == w_id).first()
	
	items_stock = {}
	for order in session.query(Order).filter(Order.whouse == whouse.id).order_by(text("id desc"))[:20]:
		for ol in order.o_lns:
			item = session.query(Item).filter(Item.id == ol.item).first()
			if item.name in items_stock.keys():
				continue
			stock = session.query(Stock).filter(Stock.warehouse == whouse.id and Stock.item == item.id).first()
			items_stock[item.name] = stock.quantity
			
	