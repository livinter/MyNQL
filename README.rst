

Install
-------

MyNLQ’s source code hosted on `GitHub <https://github.com/livinter/MyNQL>`_.

.. code-block:: bash

   git clone https://github.com/livinter/MyNQL.git
   python setup.py install

or just

.. code-block:: bash

   pip install MyNQL

Teach the Network
-----------------

For example if a customer make a purchase of a product you assume a relation between ``customer.id`` and ``product.id``,
so you connect them. Optional you can specify a distance between nodes, to represent how close the nodes are related.

* ``connect`` - connect two nodes
* ``delete`` - delete a connection

Nodes are created automatically when you do the connection, and removed if they do not have any more connections. So do not worry about them.


Ask the Network
---------------

Now you can query all kinds of relations, not only the once you taught. With select you specify a starting point, like
``customer.id`` and specify the category where you like to know its closes relation.

* ``select`` - gives you the best related nodes from a specified category

The searching query takes into account all the different routes up to a radius you specify.

Example
-------


Lets imagine we already have a table *customer*


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

and you want to teach the network about recent purchases.

.. code-block:: python

   from MyNQL import MyNQL
   mynql = MyNQL('store')

   mynql.connect('customer.juan', 'product.jeans')
   mynql.connect('customer.juan',  'product.socks')
   mynql.connect('customer.maria', 'product.socks')

If the column ``Name`` is unique you can use it as a key, otherwise you would need column ``Id``\ , and your code would look like this:

.. code-block:: python

   mynql.connect("customer.103', 'product.12')

Now you can ask questions from other points of view. You always specify a starting point, and the category where you want to know the best matches:

.. code-block:: python

   >>> mynql.select('customer.maria', 'product')
   ['socks', 'jeans']

Maria is more connected to ``socks``, as she has a direct connection, but also a bit to ``jeans`` as there exist an indirect connection through Juan.

.. code-block:: python

   >>> mynql.select('product.jeans', 'product')
   ['socks']

Any combination is valid. For example you can ask about how one product is related to other. 


Backend
-------

Storage is done in memory, but if you want to use MySQL, SQLite or PostgreSQL as a backend take a look at ``test/pee_example.py``.
This will keep a copy of all updates in your database. 
