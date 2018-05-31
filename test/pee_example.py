from MyNQL import MyNQL, utils
from peewee import *
import time

# select sqllite/postgres/mysql
db = SqliteDatabase('sample.db', pragmas={
    'journal_mode': 'wal',
    'cache_size': -1024 * 64})

class Node(Model):
    name = CharField()     # char or int
    category = CharField() # char or int 
    relation = TextField()
    class Meta:
        database = db # This model uses the "people.db" database.
        primary_key = CompositeKey('name', 'category')

def peewee_create_tables():
    with db:
        db.create_tables([Node])

def peewee_serializer(action, key, text):
    #print (time.time(),action, key)
    nam, cat = key
    if action=="INSERT":
        Node.create(name=nam, category=cat, relation=text)
    if action=="UPDATE":
        query = Node.update(relation=text).where(Node.name==nam, Node.category==cat)
        query.execute()
    if action=="DELETE":
        query = Node.delete().where(Node.name==nam, Node.category==cat)
        query.execute()

def peewee_load_network(nql):
    for node in Node.select():
       nql.load_serialized_node((node.name,node.category), node.relation)



peewee_create_tables()
mynql = MyNQL("hangango", serializer=peewee_serializer)
mynql.add_relation(("juan","person"),("email_promo1","promo"),distance= 1.)
mynql.add_relation(("juan","person"),("netbuy","tienda"),distance=1.)
mynql.add_relation(("miegel","person"),("email_promo1","promo"),distance=1.0)
mynql.add_relation(("jose","person"),("email_promo1","promo"),distance=1.0)
mynql.add_relation(("maria","person"),("netbuy","tienda"),distance=0.1)
mynql.add_relation(("maria","person"),("email_promo1","promo"),distance=1.)
mynql.set_relation(("maria","person"),("email_promo1","promo"),distance=0.1)
mynql.del_relation(("jose","person"),("email_promo1","promo"))
print(mynql.get_best_relations(("juan","person"),  "person" ))
mynql.plot()


mynql2 = MyNQL("hangango2")

peewee_load_network(mynql2)
mynql2.plot()

