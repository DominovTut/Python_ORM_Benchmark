from pony.orm import *
from datetime import datetime
from decimal import Decimal


db = Database(provider='sqlite', filename='pony.db', create_db=True)


class Warehouse(db.Entity):
	w_number = Required(int)
	w_street_1 = Required(str)
	w_street_2 = Required(str)
	w_city = Required(str)
	w_zip = Required(str)
	w_tax = Required(float)
	w_ytd = Required(float)
	
	w_orders = Set("Order")
	w_districts = Set("District")
	w_stocks = Set("Stock")
	

class District(db.Entity):
	d_id = Required(int)
	d_warehouse = Required(Warehouse)
	d_name = Required(str)
	d_street_1 = Required(str)
	d_street_2 = Required(str)
	d_city = Required(str)
	d_zip = Required(str)
	d_tax = Required(float)
	d_ytd = Required(float)
	d_orders = Set("Order")
	d_costomers = Set("Customer")


class Customer(db.Entity):
	c_first_name = Required(str)
	c_middle_name = Required(str)
	c_last_name = Required(str)
	c_street_1 = Required(str)
	c_street_2 = Required(str)
	c_city = Required(str)
	c_zip = Required(str)
	c_phone = Required(str)
	c_since = Required(datetime)
	c_credit = Required(str)
	c_credit_lim = Required(Decimal)
	c_discount = Required(float)
	c_delivery_cnt = Required(int)
	c_payment_cnt = Required(int)
	c_balance = Required(float)
	c_ytd_payment = Required(float)
	c_data1 = Required(LongStr)
	c_dtata2 = Required(LongStr)
	c_district = Required(District)
	c_orders = Set("Order")
	c_history = Set("History")
	
	
	


class Stock(db.Entity):
	s_w = Required(Warehouse)
	s_i = Required("Item")
	PrimaryKey(s_w, s_i)
	s_quantity = Required(int)
	s_ytd = Required(int)
	s_order_cnt = Required(int)
	s_remote_cnt = Required(int)
	s_data = Required(str)
	


class Item(db.Entity):
	i_name = Required(str)
	i_price = Required(float)
	i_data = Required(str)
	
	i_stock = Set(Stock)
	i_ol = Set("OrderLine")
					

class Order(db.Entity):
	o_whouse = Required(Warehouse)
	o_district = Required(District)
	o_ol_cnt = Required(int)
	o_customer = Required(Customer)
	o_entry_d = Required(datetime)
	o_o_lns = Set("OrderLine") 


class OrderLine(db.Entity):
	ol_delivery_d = Required(datetime)
	ol_item = Required(Item)
	ol_amount = Required(int)
	ol_order = Required(Order)


class History(db.Entity):
	h_date = Required(datetime)
	h_amount = Required(float)
	h_data = Required(str)
	h_customer = Required(Customer)
