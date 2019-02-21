import networkx as nx

fake_db = {}


# replace this with your favourite database
# should be a key value store, the key may be converted to/from tuple and the data-field should be text
def fake_db_serializer(action, key, text):
    global fake_db
    # the key is a tuple and can consist of integer or strings
    # print (action, key, text)
    if action == "INSERT":
        fake_db[key] = text
    if action == "UPDATE":
        fake_db[key] = text
    if action == "DELETE":
        del fake_db[key]


# node-link like in the d3.js example http://bl.ocks.org/mbostock/4062045
# use this function to save/export the network as a .json file that can be embedded as a nice html
def save_node_link_data(G, file):
    import json
    open(file, "w").write(json.dumps(nx.node_link_data(G)))
