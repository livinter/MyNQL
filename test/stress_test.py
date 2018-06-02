from random import randint
import time

import MyNQL

mynql = MyNQL.MyNQL("stress_test")

start = time.time()
N = 50000
print ("adding %i connections.." % N)
for i in range(N):
    obj1 = "tab%i.%i" % (randint(0, 20), randint(0, 10))
    obj2 = "usr%i.%i" % (randint(0, 20), randint(0, 10))
    mynql.connect(obj1, obj2)
print ("%.2f seconds" % (time.time() - start))

for i in range(5):
    print(mynql.select("usr%i.%i"% (i,1), "tab0", radius=3.)[:3])

mynql.save()
mynql.load()

