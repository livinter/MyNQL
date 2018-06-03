"""
MyNQL
=====

MyNQL is a minimalistic `graph database <https://en.wikipedia.org/wiki/Graph_database>`_ based on the `Python <http://python.org>`_ library `Networkx <https://networkx.github.io/>`_.
Instead of replacing yor relational database, it helps you to add a network with references to the data you already have.

* Nodes have the format ``table.id``
* Connections (only) have a ``distance``

You may already have tables like: Customers, merchants, products, places, areas, promotions, interests.
Those tables used to have an ``id`` that together with the table name identify each entry.

After teaching the MyNQL network relations between two ``table1.id1`` <-> ``table2.id2``,
you can ask the network also about all the **indirect** relations you like to know. A simple ``connect`` and ``select`` is all you need.

**This is very simple, but also very powerful!** You define a starting point, and search for the closest matches of a desired table.
When you add more connections your questions will stay the same, only the results will improve.
If you like to see a real live example, here is a small code for a `computer store <https://github.com/livinter/MyNQL/blob/master/test/computerstore.py#L28>`_.
The network can be serialized through `peewee <docs.peewee-orm.com>`_ to be stored on MySQL, PostgreSQL or SQLite.

Source::
    https://github.com/livinter/MyNQL
Bug reports::
    https://github.com/livinter/MyNQL/issues

"""

import logging
from logging import WARN, DEBUG, INFO
from MyNQL.MyNQL import *

