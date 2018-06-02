from MyNQL import MyNQL
from peewee import *
import os

# select SQLite/Postgres/MySQL
databse_name = 'sample.db'
db = SqliteDatabase(databse_name, pragmas={
    'journal_mode': 'wal',
    'cache_size': -1024 * 64})


class Node(Model):
    name = CharField()  # char or int
    category = CharField()  # char or int
    relation = TextField()

    class Meta:
        database = db  # This model uses the "people.db" database.
        primary_key = CompositeKey('name', 'category')


def peewee_create_tables():
    with db:
        db.create_tables([Node])


def peewee_serializer(action, key, text):
    # print (time.time(),action, key)
    cat, nam = key
    if action == "INSERT":
        Node.create(name=nam, category=cat, relation=text)
    if action == "UPDATE":
        query = Node.update(relation=text).where(Node.name == nam, Node.category == cat)
        query.execute()
    if action == "DELETE":
        query = Node.delete().where(Node.name == nam, Node.category == cat)
        query.execute()


def peewee_load_network(nql):
    for node in Node.select():
        nql.load_serialized_node((node.category, node.name), node.relation)


peewee_create_tables()
mynql = MyNQL("hangango", serializer=peewee_serializer)
mynql.connect("person.juan", "promo.email_promo1", distance=1.)
mynql.connect("person.juan", "shop.netbuy", distance=1.)
mynql.connect("person.miguel", "promo.email_promo1", distance=1.0)
mynql.connect("person.jose", "promo.email_promo1", distance=1.0)
mynql.connect("person.maria", "shop.netbuy", distance=0.1)
mynql.connect("person.maria", "promo.email_promo1", distance=1.)
mynql.delete("person.jose", "promo.email_promo1")
print(mynql.select("person.juan", "person"))
mynql.plot()

mynql2 = MyNQL("hangango_2")

peewee_load_network(mynql2)
mynql2.plot()

os.remove(databse_name)
