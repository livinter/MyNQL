from MyNQL import MyNQL
from peewee import *

# select SQLite/Postgres/MySQL
db = SqliteDatabase('sample.db', pragmas={
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
    nam, cat = key
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
        nql.load_serialized_node((node.name, node.category), node.relation)


peewee_create_tables()
mynql = MyNQL("hangango", serializer=peewee_serializer)
mynql.add(("juan", "person"), ("email_promo1", "promo"), distance=1.)
mynql.add(("juan", "person"), ("netbuy", "shop"), distance=1.)
mynql.add(("miguel", "person"), ("email_promo1", "promo"), distance=1.0)
mynql.add(("jose", "person"), ("email_promo1", "promo"), distance=1.0)
mynql.add(("maria", "person"), ("netbuy", "shop"), distance=0.1)
mynql.add(("maria", "person"), ("email_promo1", "promo"), distance=1.)
mynql.set(("maria", "person"), ("email_promo1", "promo"), distance=0.1)
mynql.delete(("jose", "person"), ("email_promo1", "promo"))
print(mynql.get(("juan", "person"), "person"))
mynql.plot()

mynql2 = MyNQL("hangango2")

peewee_load_network(mynql2)
mynql2.plot()

