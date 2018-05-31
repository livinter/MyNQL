from random import randint
#import numpy as np
import time

from MyNQL import MyNQL

mynql = MyNQL("stress_test")

start = time.time()
N=50000
#print (end="adding %i connections.."%N)
for i in range(N):
    obj1 = (randint(0,1000),randint(0,20))
    obj2 = (randint(0,1000),randint(0,20))
    mynql.add_relation(obj1, obj2, 1.)
#print ("%.2f seconds"%(time.time()-start))

for i in range(10):
    print(mynql.get_best_relations((10,i), 1 , radius=3.)[:3])

mynql.save() 
mynql.load()

