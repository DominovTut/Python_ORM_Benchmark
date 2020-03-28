from models import *
from pony.orm import *
from random import choice, randint
from datetime import datetime
from settings import AMOUNT_OF_WAREHOUSES

@db_session
def populate(n):
    citys = ('Moscow', 'St. Petersbrg', 'Pshkin', 'Oraneinbaum', 'Vladivostok')
    names = ('Ivan', 'Evgeniy', 'Alexander', 'Fedor', 'Julia', 'Stephany', 'Sergey', 'Natalya', 'Keanu', 'Jhon', 'Harry', 'James' )
    last_names = ('Petrov', 'Ivanov', 'Andreev', 'Mils', 'Smith', 'Anderson', 'Dominov', 'Tishenko', 'Zhitnikov')
    d_cnt = 0
    for i in range(1, n + 1):
        w = Warehouse(
                number=i,
                street_1='w_st %d' %i,
                street_2='w_st2 %d' %i,
                city=choice(citys),
                w_zip='w_zip %d' %i,
                tax=float(i),
                ytd=0
        )

        for j in range(10):
            District(
                warehouse=w,
                name='dist %d %d' %(w.number, j),
                street_1='d_st %d' %j,
                street_2 ='d_st2 %d' %j,
                city=w.city,
                d_zip='d_zip %d' %j,
                tax=float(j),
                ytd=0,
            )
            d_cnt +=1

    for i in range(10 * n):
        c = Customer(
            first_name=choice(names),
            middle_name=choice(names),
            last_name=choice(last_names),
            street_1='c_st %d' %i,
            street_2='c_st2 %d' %i,
            city=choice(citys),
            c_zip='c_zip %d' %i,
            phone='phone',
            since=datetime(2005, 7, 14, 12, 30),
            credit='credit',
            credit_lim=randint(1000, 100000),
            discount=choice((0, 10, 15, 20, 30)),
            delivery_cnt=0,
            payment_cnt=0,
            balance=100000,
            ytd_payment=0,
            data1='customer %d' %i,
            dtata2='hello %d'  %i,
            district=District[randint(1, 5)],
        )
        District[randint(1, 5)].customers.add(c)
    for i in range(1, n * 100 + 1):
        it = Item(
            name='item %d' %i,
            price=randint(1, 100000),
            data='data'
        )
        for j in range(1, n + 1):
            Stock(
                warehouse=Warehouse[j],
                item=it,
                quantity = 100000,
                ytd=randint(1, 100000),
                order_cnt=0,
                remote_cnt=0,
                data="data",
            )


def main():
    db.generate_mapping(create_tables=True)
    populate(AMOUNT_OF_WAREHOUSES)
	
	
if __name__ == '__main__':
    main()