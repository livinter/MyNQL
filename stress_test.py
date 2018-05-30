import random
import numpy as np
mynql = MyNQL("stress_test")

start = time.time()
N=50000
print (end="adding %i connections.."%N)
for i in range(N):
    obj1 = (np.random.randint(1000),np.random.randint(20))
    obj2 = (np.random.randint(1000),np.random.randint(20))
    mynql.add_relation(obj1, obj2, 1.)
print ("%.2f seconds"%(time.time()-start))

print(mynql.get_best_relations((10,1), 1 ))
mynql.save()
mynql.load()

