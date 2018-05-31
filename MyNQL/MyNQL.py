import logging
import time
import sys

import networkx as nx
import yaml
import mynql.utils as utils

                         
class MyNQL:
    def __init__(self, db_name, log_file=None, serializer=None):
        self.db_name = db_name
        self.G = nx.DiGraph()
        
        self.known_categorys = []
        self.serializer = serializer
        
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
        
        self.writer={"gmi":nx.write_gml, "gexf":nx.write_gexf, "gpickle": nx.write_gpickle, 
                     "graphml":nx.write_graphml, "yaml":nx.write_yaml, "node_link_data":utils.save_node_link_data}
        self.reader={"gmi":nx.read_gml, "gexf":nx.read_gexf, "gpickle": nx.read_gpickle, 
                     "graphml":nx.read_graphml, "yaml":nx.read_yaml}    
                         
    # get all categortys that have been added to the network so far
    def get_categorys(self):
        return self.known_categorys
        
    def plot(self):
        import matplotlib.pyplot as plt

        if len(self.G)>1000:
            self.logger.warning('this graph is to big to plot, plz save and visualize with gelphi.org')
            return
            
        options = {}
        options.setdefault('alpha', 0.8)
        options.setdefault('font_size', 8)
        nx.draw(self.G, with_labels=True, **options)
        plt.show()
        
    # 
    def load_serialized_node(self, key, yaml_node_data):
        self.G.add_node(key)
        edges = yaml.load(yaml_node_data)
        for edge in edges:
            self.G.add_edge(key, edge)
            attributs = edges[edge]
            for attribut in attributs:
                self.G[key][edge][attribut]=attributs[attribut]
                
    def save(self, typ="gexf", path=""):
        self.logger.debug("writing %s (%i nodes)"% (self.db_name,len(self.G)))
        typ = typ.lower()
        self.writer[typ](self.G, path+self.db_name+"."+typ)
        
    def load(self, typ="gexf", path=""):
        typ = typ.lower()        
        self.G = self.reader[typ](self.db_name+"."+typ)
        self.logger.debug("loaded %s (%i nodes)"% (self.db_name,len(self.G)))
        
    def _relation(self, obj1, obj2, distance, distance2, update_func):
        obj12 = [obj1,obj2]
        for obj in obj12:
            if type(obj)!=tuple:
                self.logger.error("key eed to be tuple")
            if len(obj)!=2:
                self.logger.error("len(key) need to be 2")
            if type(obj[0]) not in [type(""), int]:
                self.logger.error("elements need to be string or int")
            
        if not distance>0.:
            self.logger.error("distance need to be > 0")
            
        if not distance2:
                distance2 = distance/2.
        if not distance2>0.:
            self.logger.error("distance2 need to be > 0")
        
        for _,category in obj12:
            if category not in self.known_categorys:
                self.known_categorys.append(category)
                
        if self.serializer:
            for obj in obj12:
                if not obj in self.G:
                    self.serializer("INSERT",obj,"")
            
        if distance:
            if update_func:
                self.G.add_edge(obj1, obj2)
                update_func(self.G[obj1][obj2], distance)
            else:
                try:
                    self.G.remove_edge(obj1, obj2)
                except:
                    self.logger.warning('edge already removed')

        if distance2:
            if update_func:
                self.G.add_edge(obj2, obj1)
                update_func(self.G[obj2][obj1], distance2)
            else:
                try:
                    self.G.remove_edge(obj2, obj1)
                except:
                    self.logger.warning('edge already removed')
                    
        if self.serializer:
            for obj in obj12:
                self.serializer("UPDATE",obj,yaml.dump(self.G[obj]))            
                
        if not update_func:
            for obj in obj12:
                if obj in self.G:
                    if not nx.edges(self.G, obj):
                        self.G.remove_node(obj)
                        if self.serializer:
                            self.serializer("DELETE",obj,"")            
                
    def _add_edge(self, node, distance):
        if "distance" in node:
            node["distance"] = 1./(1./(distance)+1./node["distance"])
        else:
            node["distance"] = distance
            
    def _set_edge(self, node, distance):
        node["distance"] = distance
                
    def add_relation(self, obj1, obj2, distance=1., distance2=None):
        self._relation(obj1, obj2, distance, distance2, self._add_edge)                
        
    def set_relation(self, obj1, obj2, distance=1., distance2=None):
        self._relation(obj1, obj2, distance, distance2, self._set_edge)

    def del_relation(self, obj1, obj2, distance=1., distance2=None):
        self._relation(obj1, obj2, distance, distance2, None)
        
    def get_relation(self, obj1, obj2):
        if not obj1 in self.G or obj2 not in self.G:
            print(obj1, obj2, "OR not found")
            return 0.
        
        node_distance = nx.closeness_centrality(self.G, distance="distance")
        return node_distance[obj1]
        
    def get_best_relations(self, obj1, category, radius=3., in_order=True):
        if not obj1 in self.G:
            print(obj1, "not found")
            return []
        
        if category not in self.known_categorys:
            print(category, " is not know")
            return []
        # avoid a too big graph, and set center
        start = time.time()
        G2=nx.ego_graph(self.G, obj1, radius=radius, center=True, distance="distance")
        # calculate relation to obj1
        node_distance = nx.closeness_centrality(G2, distance="distance")
        # get best nodes
        best_nodes = [ (v,k) for k,v in node_distance.items() ]
        # filter to category
        best_nodes_matching = list(filter(lambda e: e[1][1]==category and e[1]!=obj1, best_nodes))
        # sort
        if in_order:
            best_nodes_matching = sorted(best_nodes_matching, reverse=True)
        self.logger.debug("get_best_relations %.2f seconds"%(time.time()-start))
        
        return best_nodes_matching

