import logging
import time
import sys
import six
import networkx as nx
import yaml
from MyNQL.utils import fake_db_serializer, save_node_link_data


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
        :param backward_factor standard multiplier from distance_backward in relation to distance
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
                       "graphml": nx.write_graphml, "yaml": nx.write_yaml, "json": save_node_link_data}
        self.reader = {"gmi": nx.read_gml, "gexf": nx.read_gexf, "gpickle": nx.read_gpickle,
                       "graphml": nx.read_graphml, "yaml": nx.read_yaml}

        # select all categories that have been added to the network so far

    def _split_node(self, node_s):
        if not isinstance(node_s, six.string_types):
            self.logger.error("please specify node as table.id")
        l = node_s.split(".")
        label = ""
        if len(l) == 2:
            pass
        elif len(l) == 3:
            label = l[2]
        else:
            self.logger.error("node need to be separated by two or three points")

        return tuple(l[:2]), label

    def get_categories(self):
        """
        all the categories that have been used so far
        >>> MyNQL("x").connect("person.juan", "promo.promo1").get_categories()
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

    def _relation(self, nodes_1, nodes_2, distance, distance_backward, update_func):
        node1, label1 = self._split_node(nodes_1)
        node2, label2 = self._split_node(nodes_2)
        node12 = [node1, node2]

        if not distance > 0.:
            self.logger.error("distance need to be > 0")

        if not distance_backward:
            distance_backward = distance * self.backward_factor
        if not distance_backward > 0.:
            self.logger.error("distance2 need to be > 0")

        for category, _ in node12:
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

        if label1:
            nx.set_node_attributes(self.G, label1, 'label')
        if label2:
            nx.set_node_attributes(self.G, label2, 'label')

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

    def connect(self, nodes1, nodes2, distance=1., distance_backward=None, rewrite=False):
        """
        connect a relation between two nodes, is the relation already exist its closeness will be reduces.
        if nodes do not exist, they will be created.

        >>> x = MyNQL("x").connect("table1.1","table2.3")
        >>> x.G[("table1","1")][("table2","3")]
        {'distance': 1.0}
        >>> _ = x.connect("table1.1","table2.3")
        >>> x.G[("table1","1")][("table2","3")]
        {'distance': 0.5}
        >>> _ = x.connect("table1.1","table2.3", rewrite=True)
        >>> x.G[("table1","1")][("table2","3")]
        {'distance': 1.0}

        :param nodes1: this is a node as a tuple composed like (name/id, category)
        :type nodes1: tuple
        :param nodes2: this is a node as a tuple composed like (name/id, category)
        :type nodes2: tuple
        :param distance: the closer the distance the more both nodes are related
        :type distance: float
        :param distance_backward:
        :type distance_backward: float
        :return:
        """
        if rewrite:
            action = self._set_edge
        else:
            action = self._add_edge
        self._relation(nodes1, nodes2, distance, distance_backward, action)
        return self


    def delete(self, nodes1, nodes2, distance=1., distance_backward=None):
        """
        >>> nql = MyNQL("x").connect("person.juan", "promo.promo1")
        >>> nql = nql.delete("person.juan", "promo.promo1")
        >>> nx.number_of_nodes(nql.G)
        0

        delete a connection. if nodes do not have any neighbour anymore, nodes are also deleted.
        :param node1:
        :param node2:
        :param distance:
        :param distance_backward:
        :return:
        """
        self._relation(nodes1, nodes2, distance, distance_backward, None)
        return self

    def get_distance(self, node1, node2, radius=3.):
        """
        select the relation between two nodes
        :param node1:
        :param node2:
        :return: float of
        """
        if node1 not in self.G:
            self.logger.error(str(node1) + " not found")
            return float('inf')
        g2 = nx.ego_graph(self.G, node1, radius=radius, center=True, distance="distance")
        if node2 not in g2:
            self.logger.debug(str(node2) + " not found")
            return float('inf')
        return nx.closeness_centrality(g2, distance="distance")[node2]

    def select(self, nodes_1, category, radius=3., in_order=True, limit=None, value_only=True):
        """
        return [(closeness, node),..] filtered by category ordered by closeness to node1
        if no nodes are found and empty list

        :param nodes_1: the starting node for calculating closeness
        :param category: the result is reduced to only elements from a specific category
        :param radius:  reduce search radius to radius
        :param in_order: sort output by having the best relation first
        :param limit:
        :param value_only:
        :return: best matching nodes
        """

        node1, label1 = self._split_node(nodes_1)

        if node1 not in self.G:
            self.logger.error(nodes_1+ " not found")
            return []

        if category not in self.known_categories:
            self.logger.error(category + " not found")
            return []
        # avoid a too big graph, and set center
        start = time.time()
        g2 = nx.ego_graph(self.G, node1, radius=radius, center=True, distance="distance")
        # calculate relation to node1
        node_distance = nx.closeness_centrality(g2, distance="distance")
        # select best nodes
        best_nodes = [(v, k) for k, v in node_distance.items()]
        # filter to category
        best_nodes_matching = filter(lambda e: e[1][0] == category and e[1] != node1, best_nodes)

        if limit == 1:
            if not best_nodes_matching:
                best_nodes_matching = []
            else:
                best_nodes_matching = [max(best_nodes_matching), ]
        else:
            if in_order:
                best_nodes_matching = sorted(best_nodes_matching, reverse=True)[:limit]

        self.logger.debug("get_best_relations %.2f seconds" % (time.time() - start))

        if value_only:
            return [table_id[1] for eval, table_id in best_nodes_matching]
        else:
            return best_nodes_matching


if __name__ == "__main__":
    import doctest

    doctest.testmod()