from MyNQL import MyNQL

mynql = MyNQL("hangango")
mynql.add_relation(("juan","person"),("email_promo1","promo"),distance= 1.)
mynql.add_relation(("juan","person"),("netbuy","tienda"),distance=1.)
mynql.add_relation(("miegel","person"),("email_promo1","promo"),distance=1.0)
mynql.add_relation(("jose","person"),("email_promo1","promo"),distance=1.0)
mynql.add_relation(("maria","person"),("netbuy","tienda"),distance=0.01)
mynql.add_relation(("maria","person"),("email_promo1","promo"),distance=0.1)
mynql.add_relation(("maria","person"),("email_promo1","promo"),distance=0.1)
print(mynql.get_best_relations(("juan","person"),  "person" ))
mynql.plot()

