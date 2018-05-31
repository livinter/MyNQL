# MyNQL

## History

This was a 15 jear old idea, now re-implemented with actual tools. At that time there was no Neo4j. But still missing something lightweight in concept and implementation.


## Concept

You tell about all the realtions you know, and ask about all the (indirect) relations you like to know.

For example you have categorys of customers, customer_attributes, merchants, merchent_attributes, products, places, areas, promotions, interests. Now you just connect what belongs together.

All nodes need to be organized as tuples in the format (name, category)

## Learn

You can do relations between those nodes using:

  * add_relation - to create or to add a relation
  * set_relation - to create or to set a relation
  * del_relation - is the relation

The nodes will be created when they have connections, and remove if they have no more connections.

Optional you can specify a distance between nodes.

## Ask

 * get_best_relation - gives you the best related nodes from a specified category
 * get_relation - tells you have good two nodes are related

To calculate how good two nodes are connected, all the different ways are taken into concideration up to a radius you can specify.

## Backend

You can put into place easily any database as a backed-storage replacing utils.fakedb_serializer. 
This will keep a copy of all updates in your database. To load the network from the database after starting use MyNQL.load_serialized_node for each node.
If you want to use MySQL, SQLite or Postgresql you can look at test/pee_example.py.





