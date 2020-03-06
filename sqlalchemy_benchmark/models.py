import os
from datetime import datetime
from decimal import Decimal

from sqlalchemy import Column, DateTime, Integer, SmallInteger, String, create_engine, ForeignKey, BigInteger, Float, Boolean, Text 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship



engine = create_engine('sqlite:////home/dominov/dev/benchmark/sqlalchemy/sqlalchemy.db')

Base = declarative_base()

class Warehouse(Base):
	__tablename__ = 'warehouse'
	
	id = Column(Integer, primary_key=True)
	number = Column(Integer, nullable=False)
	street_1 = Column(String(255), nullable=False)
	street_2 = Column(String(255), nullable=False)
	city = Column(String(255), nullable=False)
	w_zip = Column(String(255), nullable=False)
	tax = Column(Float, nullable=False)
	ytd = Column(Float, nullable=False)
	
	orders = relationship("Order") 	
	districts = relationship("District")	 
	stocks = relationship("Stock")
	

class District(Base):
	__tablename__ = 'district'
	
	id = Column(Integer, primary_key=True)
	warehouse = Column(Integer, ForeignKey('warehouse.id'))
	name = Column(String, nullable=False)
	street_1 = Column(String, nullable=False)
	street_2 = Column(String, nullable=False)
	city = Column(String, nullable=False)
	d_zip = Column(String, nullable=False)
	tax = Column(Float, nullable=False)
	ytd = Column(Float, nullable=False)
	orders = relationship("Order")
	customers = relationship("Customer")


class Customer(Base):
	__tablename__ = 'customer'
	
	id = Column(Integer, primary_key=True)
	first_name = Column(String, nullable=False)
	middle_name = Column(String, nullable=False)
	last_name = Column(String, nullable=False)
	street_1 = Column(String, nullable=False)
	street_2 = Column(String, nullable=False)
	city = Column(String, nullable=False)
	c_zip = Column(String, nullable=False)
	phone = Column(String, nullable=False)
	since = Column(DateTime, nullable=False)
	credit = Column(String, nullable=False)
	credit_lim = Column(Float, nullable=False)
	discount = Column(Float, nullable=False)
	delivery_cnt = Column(Integer, nullable=False)
	payment_cnt = Column(Integer, nullable=False)
	balance = Column(Float, nullable=False)
	ytd_payment = Column(Float, nullable=False)
	data1 = Column(Text, nullable=False)
	dtata2 = Column(Text, nullable=False)
	district = Column(Integer, ForeignKey('district.id'))
	orders = relationship("Order")
	history = relationship("History")
	
	
	


class Stock(Base):
	__tablename__ = 'stock'
	
	warehouse = Column(Integer, ForeignKey('warehouse.id'), primary_key=True)
	item = Column(Integer, ForeignKey('item.id'), primary_key=True)
	quantity = Column(Integer, nullable=False)
	ytd = Column(Integer, nullable=False)
	order_cnt = Column(Integer, nullable=False)
	remote_cnt = Column(Integer, nullable=False)
	data = Column(String, nullable=False)
	


class Item(Base):
	__tablename__ = 'item'
	
	id = Column(Integer, primary_key=True)
	name = Column(String, nullable=False)
	price = Column(Float, nullable=False)
	data = Column(String, nullable=False)
	
	stocks = relationship('Stock')
	o_lns = relationship("OrderLine")
					

class Order(Base):
	__tablename__ = 'order'
	
	id = Column(Integer, primary_key=True)
	whouse = Column(Integer, ForeignKey('warehouse.id'))
	district = Column(Integer, ForeignKey('district.id'))
	ol_cnt = Column(Integer, nullable=False)
	customer = Column(Integer, ForeignKey('customer.id'))
	entry_d = Column(DateTime, nullable=False)
	is_o_delivered = Column(Boolean, nullable=False, default=False)
	o_lns = relationship("OrderLine") 


class OrderLine(Base):
	__tablename__ = 'order_line'
	
	id = Column(Integer, primary_key=True)
	delivery_d = Column(DateTime, nullable=True)
	item = Column(Integer, ForeignKey('item.id'))
	amount = Column(Integer, nullable=False)
	order = Column(Integer, ForeignKey('order.id'))


class History(Base):
	__tablename__ = 'history'
	
	id = Column(Integer, primary_key=True)
	date = Column(DateTime, nullable=False)
	amount = Column(Float, nullable=False)
	data = Column(String, nullable=False)
	customer = Column(Integer, ForeignKey('customer.id'))


def create_tables():
    Base.metadata.create_all(engine)


