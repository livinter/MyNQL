# MyNQL


## Concept

You tell about all the realtions you know, and ask about all the (indirect) relations you like to know.

All nodes need to be organized as tuples in the format (name, category)

You can do relations between those nodes using:

  * add_relation - to create or to add a relation
  * set_relation - to create or to set a relation
  * del_relation - is the relation

The nodes will be created when they have connections, and remove if they have no more connections.

Optional you can specify a distance between nodes.

 * get_best_relation - gives you the best related nodes from a specified category
 * get_relation - tells you have good two nodes are related

To calculate how good two nodes are connected, all the different ways are taken into concideration up to a radius you can specify.

You can put into place easily any database as a backed-storage replacing utils.fakedb_serializer. This will keep a copy of all updates in your database. To load the network from the database after starting use MyNQL.load_serialized_node for each node.




