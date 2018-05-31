from MyNQL import MyNQL, utils

mynql = MyNQL("computerstore")

mynql.add_relation(("juan","person"),("Nvidia Gtx 900","producto"), distance=2.)
mynql.add_relation(("juan","person"),("Teclado","producto"), distance=2.)
mynql.add_relation(("juan","person"),("Game Pad","producto"), distance=2.)

mynql.add_relation(("maria","person"),("AMD Radeon","producto"), distance=2.)
mynql.add_relation(("maria","person"),("USB 8GB","producto"), distance=2.)
mynql.add_relation(("jose","person"),("USB 8GB","producto"), distance=2.)

mynql.add_relation(("AMD Radeon","producto"), ("video card", "product group"), distance=.5)
mynql.add_relation(("Nvidia Gtx 900","producto"), ("video card", "product group"), distance=.5)
mynql.add_relation(("USB 8GB","producto"), ("utills","product group"), distance=.5)
mynql.add_relation(("Teclado","producto"), ("computer pices","product group"), distance=.5)
mynql.add_relation(("Game Pad","producto"), ("gaming stuff","product group"), distance=.5)

mynql.add_relation(("Nvidia Gtx 900","producto"), ("lan party","promo"))
mynql.add_relation(("Game Pad","producto"), ("lan party","promo"))
mynql.add_relation(("AMD Radeon","producto"), ("lan party","promo"))

mynql.add_relation(("USB 8GB","producto"), ("office","promo"))
mynql.add_relation(("Teclado","producto"), ("office","promo"))

mynql.plot()
print ("Persons for new office promo", mynql.get_best_relations(("office","promo"),"person", radius=4.),"\n\n")
print ("Persons for video card", mynql.get_best_relations(("video card","product group"),"person", radius=4.),"\n\n")
print ("Products for Juan", mynql.get_best_relations(("juan","person"),"producto", radius=4.),"\n\n")
print ("Products related to AMD Radeon", mynql.get_best_relations(("AMD Radeon","producto"),"producto", radius=3.),"\n\n")
print ("Product Group to video card", mynql.get_best_relations(("video card","product group"),"product group", radius=3.),"\n\n")

