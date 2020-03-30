import os
from datetime import datetime
from decimal import Decimal

from sqlalchemy import Column, DateTime, Integer, SmallInteger, String, create_engine, ForeignKey, BigInteger, Float, Boolean, Text 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from settings import PROVIDER


engine = create_engine(PROVIDER['postgres'])

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
    
    orders = relationship("Order", backref='warehouse', lazy='dynamic') 	
    districts = relationship("District", backref='warehouse', lazy='dynamic')	 
    stocks = relationship("Stock", backref='warehouse', lazy='dynamic')


class District(Base):
    __tablename__ = 'district'
    
    id = Column(Integer, primary_key=True)
    warehouse_id = Column(Integer, ForeignKey('warehouse.id'), index=True)
    name = Column(String, nullable=False)
    street_1 = Column(String, nullable=False)
    street_2 = Column(String, nullable=False)
    city = Column(String, nullable=False)
    d_zip = Column(String, nullable=False)
    tax = Column(Float, nullable=False)
    ytd = Column(Float, nullable=False)
    orders = relationship("Order", backref='district', lazy='dynamic')
    customers = relationship("Customer", backref='district', lazy='dynamic')


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
    district_id = Column(Integer, ForeignKey('district.id'), index=True)
    orders = relationship("Order", backref='customer', lazy='dynamic')
    history = relationship("History", backref='customer', lazy='dynamic')


class Stock(Base):
    __tablename__ = 'stock'
    
    id = Column(Integer, primary_key=True)
    warehouse_id = Column(Integer, ForeignKey('warehouse.id'), index=True)
    item_id = Column(Integer, ForeignKey('item.id'), index=True)
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
    
    stocks = relationship('Stock', backref='item', lazy='dynamic')
    o_lns = relationship("OrderLine", backref='item', lazy='dynamic')


class Order(Base):
    __tablename__ = 'order'
    
    id = Column(Integer, primary_key=True)
    whouse_id = Column(Integer, ForeignKey('warehouse.id'), index=True)
    district_id = Column(Integer, ForeignKey('district.id'), index=True)
    ol_cnt = Column(Integer, nullable=False)
    customer_id = Column(Integer, ForeignKey('customer.id'), index=True)
    entry_d = Column(DateTime, nullable=False)
    is_o_delivered = Column(Boolean, nullable=False, default=False)
    o_lns = relationship("OrderLine", backref='order', lazy='dynamic') 


class OrderLine(Base):
    __tablename__ = 'order_line'
    
    id = Column(Integer, primary_key=True)
    delivery_d = Column(DateTime, nullable=True)
    item_id = Column(Integer, ForeignKey('item.id'), index=True)
    amount = Column(Integer, nullable=False)
    order_id = Column(Integer, ForeignKey('order.id'), index=True)

    
class History(Base):
    __tablename__ = 'history'
    
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False)
    amount = Column(Float, nullable=False)
    data = Column(String, nullable=False)
    customer_id = Column(Integer, ForeignKey('customer.id'), index=True)


def create_tables():
    Base.metadata.create_all(engine)


