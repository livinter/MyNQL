from MyNQL import MyNQL
import utils

mynql = MyNQL("hangango")
mynql.add_relation(("juan","person"),("email_promo1","promo"),distance= 1.)
mynql.add_relation(("juan","person"),("netbuy","tienda"),distance=1.)
mynql.add_relation(("miegel","person"),("email_promo1","promo"),distance=1.0)
mynql.add_relation(("jose","person"),("email_promo1","promo"),distance=1.0)
mynql.add_relation(("maria","person"),("netbuy","tienda"),distance=0.01)
mynql.add_relation(("maria","person"),("email_promo1","promo"),distance=0.1)
mynql.update_relation(("maria","person"),("email_promo1","promo"),distance=0.1)
# mynql.delete_relation(("jose","person"),("email_promo1","promo"))
print(mynql.get_best_relations(("juan","person"),  "person" ))
mynql.plot()


mynql2 = MyNQL("hangango2")

# this is how to load everything from the database back to the net
for key in utils.fake_db:
    mynql2.load_serialized_node(key, utils.fake_db[key])
    
mynql.save("gexf")
mynql.load("gexf")
mynql.save("node_link_data")
