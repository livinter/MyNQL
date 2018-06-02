from MyNQL import MyNQL

mynql = MyNQL("computer_store")

mynql.connect("customer.juan", "product.NvidiaGtx900", distance=2.)
mynql.connect("customer.juan", "product.Keyboard", distance=2.)
mynql.connect("customer.juan", "product.GamePad", distance=2.)

mynql.connect("customer.maria", "product.AMDRadeon", distance=2.)
mynql.connect("customer.maria", "product.USB8GB", distance=2.)
mynql.connect("customer.jose", "product.Keyboard", distance=2.)

# predefined product relations have a strong relation (=short distance)
mynql.connect("product.AMDRadeon", "product_group.video_card", distance=.5)
mynql.connect("product.NvidiaGtx900", "product_group.video_card", distance=.5)
mynql.connect("product.USB8GB", "product_group.utils", distance=.5)
mynql.connect("product.Keyboard", "product_group.computer_peaces",  distance=.5)
mynql.connect("product.GamePad", "product_group.gaming_stuff", distance=.5)

mynql.connect("product.NvidiaGtx900", "promo.lan_party")
mynql.connect("product.GamePad", "promo.lan_party")
mynql.connect("product.AMDRadeon", "promo.lan_party")

mynql.connect("product.USB8GB", "promo.office")
mynql.connect("product.Keyboard", "promo.office")

# mynql.plot()
print ("Customer for office promo", mynql.select("promo.office", "customer", radius=4., value_only=False))
print ("Customer for video card", mynql.select("product_group.video_card", "customer", radius=4.))
print ("Product for Juan", mynql.select("customer.juan", "product", radius=4.))
print ("Product to AMDRadeon:", mynql.select("product.AMDRadeon", "product", limit=1))
print ("Product Group to video card:", mynql.select("product_group.video_card", "product_group", limit=1))

