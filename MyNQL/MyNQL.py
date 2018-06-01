"""


"""

import logging
import time
import sys

import networkx as nx
import yaml
import mynql.utils as utils


class MyNQL:
    def __init__(self, db_name, log_file=None, serializer=None, log_level=logging.ERROR, backward_factor=.5):
        """
        create a MyNQL server

        :param db_name: name of the database
        :type db_name: string
        :param log_file: None is stdout, otherwise log filename
        :type log_file: string
        :param serializer: function to serialize all changes to database, see utils.fake_db_serializer as sample
        :param log_level: detail of logging
        :param backward_factor standard multiplicator from distance_backward in relation to distance
        :type backward_factor float
        :return:
        """
        self.db_name = db_name
        self.G = nx.DiGraph()

        self.known_categories = []
        self.serializer = serializer
        self.backward_factor = backward_factor

        self.logger = logging.getLogger("MyNQL")
        if not len(self.logger.handlers):
            if not log_file:
                fh = logging.StreamHandler(sys.stdout)
            else:
                fh = logging.FileHandler(log_file)
            formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
            fh.setFormatter(formatter)
            self.logger.addHandler(fh)
        self.logger.setLevel(level=log_level)
        self.logger.debug('Init ' + db_name)

        self.writer = {"gmi": nx.write_gml, "gexf": nx.write_gexf, "gpickle": nx.write_gpickle,
                       "graphml": nx.write_graphml, "yaml": nx.write_yaml, "json": utils.save_node_link_data}
        self.reader = {"gmi": nx.read_gml, "gexf": nx.read_gexf, "gpickle": nx.read_gpickle,
                       "graphml": nx.read_graphml, "yaml": nx.read_yaml}

        # get all categories that have been added to the network so far

    def get_categories(self):
        """
        all the categories that have been used so far
        >>> MyNQL("x").add(("juan", "person"), ("promo1", "promo")).get_categories()
        ['person', 'promo']

        :return: list of categories
        """
        return self.known_categories

    def plot(self):
        """
        draw graph using mathplotlib
        :return:
        """
        import matplotlib.pyplot as plt

        if len(self.G) > 1000:
            self.logger.warning('this graph is to big to plot, plz save and visualize with gelphi.org')
            return

        options = {}
        options.setdefault('alpha', 0.8)
        options.setdefault('font_size', 8)
        nx.draw(self.G, with_labels=True, **options)
        plt.show()


    def load_serialized_node(self, key, yaml_node_data):
        """
        used to load network from database
        :param key:
        :param yaml_node_data:
        :return:
        """
        self.G.add_node(key)
        edges = yaml.load(yaml_node_data)
        for edge in edges:
            self.G.add_edge(key, edge)
            attributes = edges[edge]
            for attribute in attributes:
                self.G[key][edge][attribute] = attributes[attribute]

    def save(self, typ="gexf", path=""):
        """
        save network to disk
        :param typ: one of gmi, gexf, gpickle, graphml, yaml, node_link_data
        :param path: location to save file
        :return:
        """
        self.logger.debug("writing %s (%i nodes)" % (self.db_name, len(self.G)))
        typ = typ.lower()
        self.writer[typ](self.G, path + self.db_name + "." + typ)

    def load(self, typ="gexf", path=""):
        """
        load the complete network

        :param typ: one of gmi, gexf, gpickle, graphml, yaml, node_link_data
        :param path: location of network file
        :return:
        """
        typ = typ.lower()
        self.G = self.reader[typ](path + self.db_name + "." + typ)
        self.logger.debug("loaded %s (%i nodes)" % (self.db_name, len(self.G)))

    def _relation(self, node1, node2, distance, distance_backward, update_func):
        node12 = [node1, node2]
        for obj in node12:
            if type(obj) != tuple:
                self.logger.error("key eed to be tuple")
            if len(obj) != 2:
                self.logger.error("len(key) need to be 2")
            if type(obj[0]) not in [type(""), int]:
                self.logger.error("elements need to be string or int")

        if not distance > 0.:
            self.logger.error("distance need to be > 0")

        if not distance_backward:
            distance_backward = distance * self.backward_factor
        if not distance_backward > 0.:
            self.logger.error("distance2 need to be > 0")

        for _, category in node12:
            if category not in self.known_categories:
                self.known_categories.append(category)

        if self.serializer:
            for obj in node12:
                if obj not in self.G:
                    self.serializer("INSERT", obj, "")

        if distance:
            if update_func:
                self.G.add_edge(node1, node2)
                update_func(self.G[node1][node2], distance)
            else:
                try:
                    self.G.remove_edge(node1, node2)
                except:
                    self.logger.warning('edge already removed')

        if distance_backward:
            if update_func:
                self.G.add_edge(node2, node1)
                update_func(self.G[node2][node1], distance_backward)
            else:
                try:
                    self.G.remove_edge(node2, node1)
                except:
                    self.logger.warning('edge already removed')

        # check for serializing updates
        if self.serializer:
            for obj in node12:
                self.serializer("UPDATE", obj, yaml.dump(self.G[obj]))

        # check for removing not used nodes
        if not update_func:
            for node in node12:
                if node in self.G:
                    if len(list(nx.all_neighbors(self.G, node))) == 0:
                        self.G.remove_node(node)
                        if self.serializer:
                            self.serializer("DELETE", node, "")

    def _add_edge(self, node, distance):
        if "distance" in node:
            node["distance"] = 1. / (1. / distance + 1. / node["distance"])
        else:
            node["distance"] = distance

    def _set_edge(self, node, distance):
        node["distance"] = distance

    def add(self, node1, node2, distance=1., distance_backward=None):
        """
        add a relation between two nodes, is the relation already exist its closeness will be reduces

        >>> x = MyNQL("x").add((1,1),(3,3))
        >>> x.G[(1,1)][(3,3)]
        {'distance': 1.0}
        >>> _ = x.add((1,1),(3,3))
        >>> x.G[(1,1)][(3,3)]
        {'distance': 0.5}


        :param node1: this is a node as a tuple composed like (name/id, category)
        :type node1: tuple
        :param node2: this is a node as a tuple composed like (name/id, category)
        :type node2: tuple
        :param distance: the closer the distance the more both nodes are related
        :type distance: float
        :param distance_backward:
        :type distance_backward: float
        :return:
        """
        self._relation(node1, node2, distance, distance_backward, self._add_edge)
        return self

    def set(self, node1, node2, distance=1., distance_backward=None):
        """
        >>> x = MyNQL("x").set((1,1),(3,3))
        >>> x.G[(1,1)][(3,3)]
        {'distance': 1.0}
        >>> _ = x.set((1,1),(3,3))
        >>> x.G[(1,1)][(3,3)]
        {'distance': 1.0}

        set a relation between two nodes, is the relation already exist its closeness will be overwritten
        :param node1: this is a node as a tuple composed like (name/id, category)
        :type node1: tuple
        :param node2: this is a node as a tuple composed like (name/id, category)
        :type node2: tuple
        :param distance: the closer the distance the more both nodes are related
        :type distance: float
        :param distance_backward:
        :type distance_backward: float
        :return:
        """
        self._relation(node1, node2, distance, distance_backward, self._set_edge)
        return self

    def delete(self, node1, node2, distance=1., distance_backward=None):
        """
        >>> nql = MyNQL("x").add(("juan", "person"), ("promo1", "promo"))
        >>> nql = nql.delete(("juan", "person"), ("promo1", "promo"))
        >>> nx.number_of_nodes(nql.G)
        0

        delete a connection
        :param node1:
        :param node2:
        :param distance:
        :param distance_backward:
        :return:
        """
        self._relation(node1, node2, distance, distance_backward, None)
        return self

    def get_distance(self, node1, node2, radius=3.):
        """
        get the relation between two nodes
        :param node1:
        :param node2:
        :return: float of
        """
        if node1 not in self.G:
            self.logger.error(str(node1)+" not found")
            return float('inf')
        g2 = nx.ego_graph(self.G, node1, radius=radius, center=True, distance="distance")
        if node2 not in g2:
            self.logger.debug(str(node2)+" not found")
            return float('inf')
        return nx.closeness_centrality(g2, distance="distance")[node2]

    def _get(self, node1, category, radius, in_order=True, best_only=False):

        if node1 not in self.G:
            self.logger.error(str(node1)+" not found")
            return []

        if category not in self.known_categories:
            self.logger.error(str(category)+" not found")
            return []
        # avoid a too big graph, and set center
        start = time.time()
        g2 = nx.ego_graph(self.G, node1, radius=radius, center=True, distance="distance")
        # calculate relation to node1
        node_distance = nx.closeness_centrality(g2, distance="distance")
        # get best nodes
        best_nodes = [(v, k) for k, v in node_distance.items()]
        # filter to category
        best_nodes_matching = filter(lambda e: e[1][1] == category and e[1] != node1, best_nodes)

        if best_only:
            if not best_nodes_matching:
                return None
            else:
                return max(best_nodes_matching)[1][0]

        if in_order:
            best_nodes_matching = sorted(best_nodes_matching, reverse=True)
        self.logger.debug("get_best_relations %.2f seconds" % (time.time() - start))

        return best_nodes_matching

    def get(self, node1, category, radius=3., in_order=True):
        """
        return [(closeness, node),..] filtered by category ordered by closeness to node1
        if no nodes are found and empty list

        :param node1: the starting node for calculating closeness
        :type: tuple
        :param category: the result is reduced to only elements from a specific category
        :type: string
        :param radius: reduce search radius to radius
        :type: float
        :param in_order: sort output by having the best relation first
        :type: bool
        :return: best matching nodes
        """
        return self._get(node1, category, radius, in_order)

    def get_best(self, node1, category, radius=3.):
        """
        return just the best matching node value, if no node has been found None is returned
        :param node1:
        :param category:
        :param radius:
        :return:
        """
        return self._get(node1, category, radius, best_only=True)


if __name__ == "__main__":
    import doctest
    doctest.testmod()