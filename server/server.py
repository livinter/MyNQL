from os import environ
import time

from xmlrpc.server import SimpleXMLRPCServer

from peewee import SqliteDatabase, Model, CharField, TextField, CompositeKey

from MyNQL import MyNQL


def get_environment(env_name, default):
    if env_name in environ:
        return environ.get(env_name)
    else:
        return default


db_type = get_environment("MYNQL_DB_TYPE", 'sqlite')
name = get_environment("MYNQL_DB_NAME", 'hangango')
database_name = name + '.db'
server = get_environment("MYNQL_HOST", "localhost")
port = int(get_environment("MYNQL_PORT", 8000))
mynql_log_file = get_environment("MYNQL_LOGFILE", None)

if db_type == "sqlite":
    db = SqliteDatabase(database_name, pragmas={
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
    cat, nam = key
    if action == "INSERT":
        Node.create(name=nam, category=cat, relation=text)
    if action == "UPDATE":
        query = Node.update(relation=text).where(Node.name == nam, Node.category == cat)
        query.execute()
    if action == "DELETE":
        query = Node.delete().where(Node.name == nam, Node.category == cat)
        query.execute()
    return True


def peewee_load_network(nql):
    for node in Node.select():
        nql.load_serialized_node((node.category, node.name), node.relation)


try:
    peewee_create_tables()
except:
    print("already created?")
    pass

mynql = MyNQL(name, serializer=peewee_serializer, log_file=mynql_log_file)

try:
    peewee_load_network(mynql)
    print("network loaded")
except:
    print("can not load old network")
    pass


def connect(kwargs):
    mynql.connect(**kwargs)
    return True


def select(kwargs):
    ret = mynql.select(**kwargs)
    print("select return", ret)
    return ret


def delete(kwargs):
    mynql.delete(**kwargs)
    return True


def get_categories():
    return mynql.get_categories()


def get_distance(kwargs):
    return mynql.get_distance(**kwargs)


def save(kwargs):
    mynql.save(**kwargs)
    return True


def load(kwargs):
    mynql.load(**kwargs)
    return True


def plot():
    mynql.plot()
    return True


server = SimpleXMLRPCServer((server, port))
print("Listening on port " + str(port) + "...")
server.register_function(connect, 'connect')
server.register_function(select, 'select')
server.register_function(get_distance, 'get_distance')
server.register_function(delete, 'delete')
server.register_function(get_categories, 'get_categories')
server.register_function(save, 'save')
server.register_function(load, 'load')
server.register_function(plot, 'plot')

server.serve_forever()
