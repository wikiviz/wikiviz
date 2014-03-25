# model.py
from kivy.event import EventDispatcher
import wikiviz.common.singleton as singleton
# import wikiviz.display.display as display


class Model(EventDispatcher):
    __metaclass__ = singleton.Singleton

    def __init__(self, **kwargs):
        """
         Creates empty model of nodes and edges, prepares to dispatch when updated
        """
        self.register_event_type('on_update')
        super(Model, self).__init__(**kwargs)
        self.nodes = []
        self.edges = []

    def add_node(self, node):
        self.nodes.append(node)
        self.dispatch('on_update', node)

    def add_edge(self, edge):
        self.edges.append(edge)

    def print_graph(self):
        print "Printing graph in model"
        for n in self.nodes:
            print "Node: ", n
            print n.links, "\n"
        for e in self.edges:
            print "Edge: ", e
        print "\n"

    def on_update(self, *args):
        pass
        # print "updated - event was dispatched", args
        # TODO: Re-hookup display notifications
        # d = display.Display()
        # d.trigger_update()


class Node():
    def __str__(self):
        return ':\t'.join([self.keyword, self.href])

    def __init__(self, keyword, href, img_src, text, links, has_visited=False):
        self.keyword = keyword
        self.href = href
        self.img_src = img_src
        self.text = text
        self.links = links
        self.has_visited = has_visited


class Edge():
    def __str__(self):
        return ', '.join([self.source, self.destination])

    def __init__(self, source, destination):
        self.source = source
        self.destination = destination

