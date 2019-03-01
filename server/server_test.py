import xmlrpc.client
with xmlrpc.client.ServerProxy("http://localhost:8000/") as mynql:
    mynql.connect(dict(nodes1=("person","juan"), nodes2=("promo","email_promo1"), distance=1))
    mynql.connect(dict(nodes1="person.miguel", nodes2="promo.email_promo1", distance=1))
    mynql.connect(dict(nodes1="person.jose", nodes2="promo.email_promo1", distance=1))
    mynql.connect(dict(nodes1="person.maria", nodes2="shop.netbuy", distance=0.1))
    mynql.connect(dict(nodes1="person.maria", nodes2="promo.email_promo1", distance=1))
    mynql.delete(dict(nodes1="person.jose", nodes2="promo.email_promo1"))

    print("get other persons related to juan:")
    print(mynql.select(dict(nodes_1=("person","juan"), category="person")))

print("start new connection, expecting to plot same old data")
with xmlrpc.client.ServerProxy("http://localhost:8000/") as mynql2:
    mynql2.plot()


