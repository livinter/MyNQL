# MyNQL


## Concept


All nodes need to be organized as tuples in the format (name, category)

You can do relations between those nodes using:

  * add_relation - to create or to add a relation
  * update_relation - to create or to set a relation
  * delete_relation - is the relation

The nodes will be created when they have connections, and remove if they have no more connections.

Optional you can specify a distance between nodes.

 * get_best_relation - gives you the best related nodes from a specified category
 * get_relation - tells you have good two nodes are related

The network takes in account the manmy different relations that may exist.


