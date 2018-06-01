from random import randint
import time

from MyNQL import MyNQL

mynql = MyNQL("stress_test")

start = time.time()
N=50000
print ("adding %i connections.."%N)
for i in range(N):
    obj1 = (randint(0,1000),randint(0,20))
    obj2 = (randint(0,1000),randint(0,20))
    mynql.add(obj1, obj2, 1.)
print ("%.2f seconds"%(time.time()-start))

for i in range(5):
    print(mynql.get((10,i), 1 , radius=3.)[:3])

mynql.save()
mynql.load()

