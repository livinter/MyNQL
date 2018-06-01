from MyNQL import MyNQL, utils

mynql = MyNQL("hangango", serializer=utils.fake_db_serializer)
mynql.add(("juan", "person"), ("email_promo1", "promo"), distance=1.)
mynql.add(("juan", "person"), ("netbuy", "shop"), distance=1.)
mynql.add(("miguel", "person"), ("email_promo1", "promo"), distance=1.0)
mynql.add(("jose", "person"), ("email_promo1", "promo"), distance=1.0)
mynql.add(("maria", "person"), ("netbuy", "shop"), distance=0.01)
mynql.add(("maria", "person"), ("email_promo1", "promo"), distance=0.1)
mynql.set(("maria", "person"), ("email_promo1", "promo"), distance=0.1)
mynql.delete(("jose", "person"), ("email_promo1", "promo"))
print(mynql.get(("juan", "person"), "person"))
mynql.plot()

mynql2 = MyNQL("hangango2")

# this is how to load everything from the database back to the net
for key in utils.fake_db:
    mynql2.load_serialized_node(key, utils.fake_db[key])

mynql.save("gexf")
mynql.load("gexf")
mynql.save("json")
