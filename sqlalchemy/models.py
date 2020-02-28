import os
from datetime import datetime
from decimal import Decimal

from sqlalchemy import Column, DateTime, Integer, SmallInteger, String, create_engine, ForeignKey, BigInteger, Float, Numeric, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship



engine = create_engine('sqlite:////home/dominov/dev/benchmark/sqlalchemy/sqlalchemy.db')

Base = declarative_base()

class Warehouse(Base):
	__tablename__ = 'warehouse'
	
	id = Column(Integer, primary_key=True)
	w_number = Column(Integer, nullable=False)
	w_street_1 = Column(String(255), nullable=False)
	w_street_2 = Column(String(255), nullable=False)
	w_city = Column(String(255), nullable=False)
	w_zip = Column(String(255), nullable=False)
	w_tax = Column(Float, nullable=False)
	w_yid = Column(Float, nullable=False)
	
	w_orders = relationship("Order") 	
	w_districts = relationship("District")	 
	w_stocks = relationship("Stock")
	

class District(Base):
	__tablename__ = 'district'
	
	id = Column(Integer, primary_key=True)
	d_warehouse = Column(Integer, ForeignKey('warehouse.id'))
	d_name = Column(String, nullable=False)
	d_street_1 = Column(String, nullable=False)
	d_street_2 = Column(String, nullable=False)
	d_city = Column(String, nullable=False)
	d_zip = Column(String, nullable=False)
	d_tax = Column(Float, nullable=False)
	d_yid = Column(Float, nullable=False)
	d_orders = relationship("Order")
	d_costomers = relationship("Customer")


class Customer(Base):
	__tablename__ = 'customer'
	
	id = Column(Integer, primary_key=True)
	c_first_name = Column(String, nullable=False)
	c_middle_name = Column(String, nullable=False)
	c_last_name = Column(String, nullable=False)
	c_street_1 = Column(String, nullable=False)
	c_street_2 = Column(String, nullable=False)
	c_city = Column(String, nullable=False)
	c_zip = Column(String, nullable=False)
	c_phone = Column(String, nullable=False)
	c_since = Column(DateTime, nullable=False)
	c_credit = Column(String, nullable=False)
	c_credit_lim = Column(Float, nullable=False)
	c_discount = Column(Float, nullable=False)
	c_delivery_cnt = Column(Integer, nullable=False)
	c_payment_cnt = Column(Integer, nullable=False)
	c_balance = Column(Float, nullable=False)
	c_ytd_payment = Column(Float, nullable=False)
	c_data1 = Column(Text, nullable=False)
	c_dtata2 = Column(Text, nullable=False)
	c_district = Column(Integer, ForeignKey('district.id'))
	c_orders = relationship("Order")
	c_history = relationship("History")
	
	
	


class Stock(Base):
	__tablename__ = 'stock'
	
	s_w = Column(Integer, ForeignKey('warehouse.id'), primary_key=True)
	s_i = Column(Integer, ForeignKey('item.id'), primary_key=True)
	s_quantity = Column(Integer, nullable=False)
	s_ytd = Column(Integer, nullable=False)
	s_order_cnt = Column(Integer, nullable=False)
	s_remote_cnt = Column(Integer, nullable=False)
	s_data = Column(String, nullable=False)
	


class Item(Base):
	__tablename__ = 'item'
	
	id = Column(Integer, primary_key=True)
	i_name = Column(String, nullable=False)
	i_price = Column(Float, nullable=False)
	i_data = Column(String, nullable=False)
	
	i_stocks = relationship('Stock')
	i_ols = relationship("OrderLine")
					

class Order(Base):
	__tablename__ = 'order'
	
	id = Column(Integer, primary_key=True)
	o_whouse = Column(Integer, ForeignKey('warehouse.id'))
	o_district = Column(Integer, ForeignKey('district.id'))
	o_ol_cnt = Column(Integer, nullable=False)
	o_customer = Column(Integer, ForeignKey('customer.id'))
	o_entry_d = Column(DateTime, nullable=False)
	o_o_lns = relationship("OrderLine") 


class OrderLine(Base):
	__tablename__ = 'order_line'
	
	id = Column(Integer, primary_key=True)
	ol_delivery_d = Column(DateTime, nullable=False)
	ol_item = Column(Integer, ForeignKey('item.id'))
	ol_amount = Column(Integer, nullable=False)
	ol_order = Column(Integer, ForeignKey('order.id'))


class History(Base):
	__tablename__ = 'history'
	
	id = Column(Integer, primary_key=True)
	h_date = Column(DateTime, nullable=False)
	h_amount = Column(Float, nullable=False)
	h_data = Column(String, nullable=False)
	h_customer = Column(Integer, ForeignKey('customer.id'))


def create_tables():
    Base.metadata.create_all(engine)


if __name__ == '__main__':
	create_tables()