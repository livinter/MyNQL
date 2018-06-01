# MyNQL


## Concept

A good foundation is a simple concept:
 * Nodes have a type/category and a id/key
 * Connections only have a distance
 
You may have types/categories like: customers, customer_attributes, merchants, merchant_attributes, products, 
places, areas, promotions, interests. This categories are often the name of the tables in your relational database.
Each entry in your database used to have an id/key.

As every item in your database can be identified this way, all nodes need to be organized as tuples in the format `(id/key/name, type/category)`

Now teach the network by telling all the known relations, and ask the network about all the (indirect) relations you like to know.

**This is very simple, but also very powerful!** You define a starting point, and search for the closest matches of a desired type/category.
When you add more connections your questions will stay the same, only the results will improve.
If you like to see a real live example look this example.
https://github.com/livinter/MyNQL/blob/master/test/computerstore.py#L28




## Install
```
git clone https://github.com/livinter/MyNQL.git
python setup.py install
```


## Teach the Network

You can do relations between those nodes using:

  * `add` - to create or to add a relation
  * `set` - to create or to set a relation
  * `delete` - delete a relation

The nodes will be created when they have connections, and remove if they have no more connections.

Optional you can specify a distance between nodes.

## Ask the network

  * `get` - gives you the best related nodes from a specified category
  * `get_best` - tells you have good two nodes are related

To calculate how good two nodes are connected, all the different ways are taken into consideration up to a radius you can specify.


## Design

Imagen you have

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

First you teach your network:

```
from MyNQL import MyNQL
mynql = MyNQL("computerstore")

mynql.add(("Juan", "customer"), ("jeans", "product"))
mynql.add(("Juan", "customer"), ("socks", "product"))
mynql.add(("Maria", "customer"), ("socks", "product"))
```

Then you can ask questions from other points of view.
You always specify a starting point, and the category where you want to know the best matches.
```

products_related_to_juan = mynql.get(("Juan", "customer"), ("product"))
products_related_to_jeans = mynql.get(("jeans", "product"), ("product"))

```


## Back-end

You can put into place easily any database as a backed-storage replacing `utils.fakedb_serializer.`
This will keep a copy of all updates in your database. To load the network from the database after starting use MyNQL.`load_serialized_node` for each node.
If you want to use MySQL, SQLite or Postgresql you can look at `test/pee_example.py`.



