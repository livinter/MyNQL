# MyNQL

## History

A lightweight concept and implementation for recomendation.


## Concept

You tell about all the relations you know, and ask about all the (indirect) relations you like to know.

For example you have categories of customers, customer_attributes, merchants, merchant_attributes, products, places, areas, promotions, interests. Now you just connect what belongs together.

All nodes need to be organized as tuples in the format `(name, category)`

## Install
```
https://github.com/livinter/MyNQL.git
python setup.py install
```


## Teach the Network

You can do relations between those nodes using:

  * `add` - to create or to add a relation
  * `set` - to create or to set a relation
  * `delete` - delete the relation

The nodes will be created when they have connections, and remove if they have no more connections.

Optional you can specify a distance between nodes.

## Ask the network

  * `get` - gives you the best related nodes from a specified category
  * `get_best` - tells you have good two nodes are related

To calculate how good two nodes are connected, all the different ways are taken into consideration up to a radius you can specify.


## Design

Lets imagen you have

Table *customer*
| Id      | Name     | ..  |
| ------- | -------- | --- |
| 101     | Jose     | ... |
| 102     | Maria    | ... |
| 103     | Juan     | ... |
....

Table *product*
| Id      | Name     | ..  |
| ------- | -------- | --- |
| 101     | jeans    | ... |
| 102     | heat     | ... |
| 103     | socks    | ... |
....


And you want to discover new relations.

First you teach your network

```
from MyNQL import MyNQL
mynql = MyNQL("computerstore")

mynql.add(("Juan", "customer"), ("jeans", "product"))
mynql.add(("Juan", "customer"), ("socks", "product"))
mynql.add(("Maria", "customer"), ("socks", "product"))

```


## Back-end

You can put into place easily any database as a backed-storage replacing `utils.fakedb_serializer.`
This will keep a copy of all updates in your database. To load the network from the database after starting use MyNQL.`load_serialized_node` for each node.
If you want to use MySQL, SQLite or Postgresql you can look at `test/pee_example.py`.



