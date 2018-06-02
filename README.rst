
MyNQL
=====

Concept
-------

**A good foundation is a simple concept:** 


* Nodes have the format ``table.id`` 
* Connections have a ``distance``

You may already have tables like: customers, merchants, products, places, areas, promotions, interests. 
Most of the times in a relational database there is an id/key, so with ``table.id`` all entries can be addressed.

Teach the MyNQL network relations between two ``table1.id1`` <-> ``table2.id2`` you know,
and then ask the network about all the (indirect) relations you like to know.

**This is very simple, but also very powerful!** You define a starting point, and search for the closest matches of a desired table.
When you add more connections your questions will stay the same, only the results will improve.
If you like to see a real live example look this example, here is an example with a `Computer Store <https://github.com/livinter/MyNQL/blob/master/test/computerstore.py#L28>`_.

Install
-------

.. code-block:: bash

   git clone https://github.com/livinter/MyNQL.git
   python setup.py install

Teach the Network
-----------------

You can do relations between those nodes using:


* ``connect`` - connect two nodes
* ``delete`` - delete a connection

The nodes will be created when they have connections, and remove if they have no more connections.

Optional you can specify a distance between nodes.

Ask the network
---------------


* ``select`` - gives you the best related nodes from a specified category

To calculate how good two nodes are connected, all the different ways are taken into consideration up to a radius you specify.

Design
------

Imagen you have

Table *customer*

.. list-table::
   :header-rows: 1

   * - Id
     - Name
     - ..
   * - 101
     - jose
     - ...
   * - 102
     - maria
     - ...
   * - 103
     - juan
     - ...


And you want to discover new relations.

First you teach your network.

.. code-block:: python

   from MyNQL import MyNQL
   mynql = MyNQL('store')

   mynql.connect('customer.juan', 'product.jeans')
   mynql.connect('customer.juan',  'product.socks')
   mynql.connect('customer.maria', 'product.socks')

If the colum ``Name`` is unique you can use it as a key, otherwise you would need colum ``Id``\ , and your code would look like this: 

.. code-block:: python

   mynql.connect("customer.103', 'product.12')

Now you can ask questions from other points of view. You always specify a starting point, and the category where you want to know the best matches:

.. code-block:: python

   >>> mynql.select('customer.maria', 'product')
   ['socks', 'jeans']

Maria is more connected to ``socks``\ , as she has a direct connection, but also a bit to ``jeans`` as there exist an indirect connection through Juan.

.. code-block:: python

   >>> mynql.select('product.jeans', 'product')
   ['socks']

Any combination is valid. For example you can ask about how one product is related to other. 

Back-end
--------

Storage is done in memory, but if you want to use MySQL, SQLite or Postgresql as a backend take a look at ``test/pee_example.py``.
This will keep a copy of all updates in your database. 
