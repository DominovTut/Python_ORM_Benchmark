from models import *
from random import randint, choice
from datetime import datetime
from pony.orm import *



@db_session(retry=10)
def new_order_tran(w_id, c_id):
	whouse = Warehouse[w_id]
	district = choice(list(select(d for d in District if d.warehouse == whouse)))	
	customer = Customer[c_id]
	ol_cnt = randint(1, 10)
	amount = randint(1, 10)
	
	order = Order(
		ol_cnt=ol_cnt,
		customer=customer,
		entry_d=datetime.now(),
		warehouse=whouse,
		district=district
	)
	items = []
	for i in range(ol_cnt):
		item = Item[randint(1, 100)]
		items.append(item)
		ord_line = OrderLine(
			item=item,
			amount=amount,
			order=order
		)
	stocks = select(stock for stock in Stock 
					if stock.warehouse == whouse and stock.item in items).order_by(Stock.id).for_update()
	for stock in stocks:
		stock.order_cnt += 1
		stock.quantity -= amount


		
		

	


@db_session(retry=10)
def payment_tran(w_id, c_id):
	whouse = Warehouse[w_id]
	district = choice(list(select(d for d in District if d.warehouse == whouse)))
	customer = Customer[c_id]
	h_amount = randint(10, 5000)
	
	whouse.ytd += h_amount
	district.ytd += h_amount
	customer.balance -= h_amount
	customer.ytd_payment += h_amount
	customer.payment_cnt += 1
	
	History(
		date=datetime.now(),
		amount=h_amount,
		data='new_paynment',
		customer=customer,
	)	
		
	
	


@db_session(retry=10)
def order_status_tran(c_id):
	customer = Customer[c_id]
	last_order = customer.orders.select().order_by(lambda o: desc(o.id)).first()
	o_ls = []
	if not last_order:
		commit()
		return
	status = last_order.is_o_delivered
	for ol in last_order.o_lns:
		o_ls.append({
			'delivery_d' : ol.delivery_d,
			'item' : ol.item,
			'amount' : ol.amount,
			'order' : ol.order
		})

		

	


@db_session(retry=10)
def delivery_tran(w_id):
	whouse = Warehouse[w_id]
	o_c = []
	districts = select(d for d in District if d.warehouse == whouse).order_by(District.id).for_update()
	for district in districts:
		order = select(o for o in Order if o.district == district and o.is_o_delivered == False).order_by(Order.id)	.first()
		if not order:
			return
		order.is_o_delivered = True
		for o_l in order.o_lns:
			o_l.delivery_d = datetime.now()
		o_c.append(order.customer)
	customers = select(c for c in Customer if c in o_c).for_update()
	for customer in customers:
		customer.delivery_cnt += 1
		
	


@db_session(retry=10)
def stock_level_tran(w_id):
	whouse = Warehouse[w_id]
	orders = select(o for o in Order if o.warehouse == whouse).order_by(lambda o: desc(o.id))[:20]
	items_stock = {}
	for order in orders:
		for ol in order.o_lns:
			item_name = ol.item.name
			if item_name in items_stock.keys():
				continue
			stock = select(s for s in Stock if s.warehouse == whouse and s.item == ol.item).first()
			items_stock[item_name] = stock.quantity
	
	
	