 Most of the time ORM are used in web applications, where more than one user sends all kinds of queries to database at the same time, but I could not find any benchmarks that rate performance of Python ORMs in a scenario like this. As a result, I decided to write my own  benchmark and compare PonyORM and SQLAlchemy with it. As a basis, I took the TPC-C benchmark.

This benchmark is based on the TPC-C benchmark and is adapted for testing Python ORMs. The test database represents a warehouse network. Five different types of transactions are submitted to the database with different probabilities. The test measures how many transactions are processed per minute. Also, this benchmark estimates the performance on each individual transaction.

<b>Transactions:</b><br>
1.new_order - 45%<br>
2.payment - 43%<br>
3.order_status - 4%<br>
4.delivery - 4%<br>
5.stock_level - 4%

The benchmark is currently written for SQLAlchemy and PonyORM.

below you can see the results of the test. Each test ran for 10 minutes with two virtual users. 
The values below are the average number of transactions per minute.

<b>Results:</b>

<b>All transactions</b>
```
PonyORM: 2543
SQLAlchemy: 1353.4
```
<b>new_order</b>
```
PonyORM: 3349.2
SQLAlchemy: `1415.3`
```
<b>payment</b>
```
PonyORM: 7175.3
SQLAlchemy: 4110.6
```
<b>order_status:</b>
```
PonyORM: 16645.6
SQLAlchemy: 4820.8
```
<b>delivery</b>
```
PonyORM: 323.5
SQLAlchemy: 716.9
```
<b>stock_level</b>
```
PonyORM: 677.3
SQLAlchemy: 167.9
```





