from MyNQL import MyNQL

mynql = MyNQL("computerstore")

mynql.add(("juan", "customer"), ("Nvidia Gtx 900", "product"), distance=2.)
mynql.add(("juan", "customer"), ("Teclado", "product"), distance=2.)
mynql.add(("juan", "customer"), ("Game Pad", "product"), distance=2.)

mynql.add(("maria", "customer"), ("AMD Radeon", "product"), distance=2.)
mynql.add(("maria", "customer"), ("USB 8GB", "product"), distance=2.)
mynql.add(("jose", "customer"), ("USB 8GB", "product"), distance=2.)

# predefined product relations have a strong relation (=short distance)
mynql.add(("AMD Radeon", "product"), ("video card", "product group"), distance=.5)
mynql.add(("Nvidia Gtx 900", "product"), ("video card", "product group"), distance=.5)
mynql.add(("USB 8GB", "product"), ("utills", "product group"), distance=.5)
mynql.add(("Teclado", "product"), ("computer pices", "product group"), distance=.5)
mynql.add(("Game Pad", "product"), ("gaming stuff", "product group"), distance=.5)

mynql.add(("Nvidia Gtx 900", "product"), ("lan party", "promo"))
mynql.add(("Game Pad", "product"), ("lan party", "promo"))
mynql.add(("AMD Radeon", "product"), ("lan party", "promo"))

mynql.add(("USB 8GB", "product"), ("office", "promo"))
mynql.add(("Teclado", "product"), ("office", "promo"))

mynql.plot()
print ("customer for new office promo", mynql.get(("office", "promo"), "customer", radius=4.), "\n\n")
print ("customer for video card", mynql.get(("video card", "product group"), "customer", radius=4.), "\n\n")
print ("Products for Juan", mynql.get(("juan", "customer"), "product", radius=4.), "\n\n")
print ("Product to AMD Radeon:", mynql.get_best(("AMD Radeon", "product"), "product"), "\n\n")
print ("Product Group to video card:", mynql.get_best(("video card", "product group"), "product group"), "\n\n")

