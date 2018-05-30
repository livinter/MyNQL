import matplotlib.pyplot as plt
import networkx as nx
import logging
import time
import sys

class MyNQL:
    def __init__(self, db_name, log_file=None):
        self.db_name = db_name
        self.G = nx.DiGraph()
        
        self.known_categorys = []
        
        self.logger = logging.getLogger("MyNQL")
        if not len(self.logger.handlers):
            if not log_file:
                fh = logging.StreamHandler(sys.stdout)
            else:
                fh = logging.FileHandler(log_file)
            formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
            fh.setFormatter(formatter)
            self.logger.addHandler(fh)
        self.logger.setLevel(level=logging.DEBUG)
        self.logger.debug('Init '+ db_name)
        
    def plot(self):
        if len(self.G)>1000:
            self.logger.warning('this graph is to big to plot')
            return
            
        options = {}
        options.setdefault('alpha', 0.8)
        options.setdefault('font_size', 8)
        nx.draw(self.G, with_labels=True,  **options)
        plt.show()
        
    def save(self):
        self.logger.debug("writing %s (%i nodes)"% (self.db_name,len(self.G)))
        nx.write_gexf(self.G, self.db_name)
        
    def load(self):
        self.G = nx.read_gexf(self.db_name)
        self.logger.debug("loaded %s (%i nodes)"% (self.db_name,len(self.G)))
        
    def add_relation(self, obj1, obj2, distance=1., distance2=None):
        """
        obj1 tuple (name, category)
        obj2 tuple (name, category)
        """
        assert(len(obj1)==2)
        assert(len(obj2)==2)
        assert(distance>0.)
        if not distance2:
                distance2 = distance/2.
        assert(distance2>0.)
        
        if obj1[1] not in self.known_categorys:
            self.known_categorys.append(obj1[1])
        if obj2[1] not in self.known_categorys:
            self.known_categorys.append(obj2[1])
        
        if distance:
            self.G.add_edge(obj1, obj2)
            if "distance" in self.G[obj1][obj2]:
                self.G[obj1][obj2]["distance"] = 1./(1./(distance)+1./self.G[obj1][obj2]["distance"])
            else:
                self.G[obj1][obj2]["distance"] = distance
                
        if distance2:
            self.G.add_edge(obj2, obj1)
            if "distance" in self.G[obj2][obj1]:
                self.G[obj2][obj1]["distance"] =1./(1./(distance2)+1./self.G[obj2][obj1]["distance"])
            else:
                self.G[obj2][obj1]["distance"] = distance2
                
    def get_relation(self, obj1, obj2):
        if not obj1 in self.G or obj2 not in self.G:
            print(obj1, obj2, "OR not found")
            return 0.
        
        node_distance = nx.closeness_centrality(self.G, distance="distance")
        return node_distance[obj1]
        
    def get_best_relations(self, obj1, category, radius=4):
        if not obj1 in self.G:
            print(obj1, "not found")
            return []
        
        if category not in self.known_categorys:
            print(category, " is not know")
            return []
        # avoid a too big graph, and set center
        start = time.time()
        G2=nx.ego_graph(self.G, obj1, radius=radius, center=True)
        # calculate relation to obj1
        node_distance = nx.closeness_centrality(G2, distance="distance")
        # get best nodes
        best_nodes = sorted([ (v,k) for k,v in node_distance.items() ])[::-1]
        # filter to category
        best_nodes_matching = list(filter(lambda e: e[1][1]==category and e[1]!=obj1, best_nodes))
        self.logger.debug("get_best_relations %.2f seconds"%(time.time()-start))
        
        return best_nodes_matching  

