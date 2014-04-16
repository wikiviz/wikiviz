# model.py
from kivy.event import EventDispatcher
import common.singleton as singleton



class Model(EventDispatcher):
    __metaclass__ = singleton.Singleton

    def __init__(self, **kwargs):
        """
         Creates empty model of nodes and edges, prepares to dispatch when updated
        """
        super(Model, self).__init__(**kwargs)
        self.nodes = []
        self.x = 0
        self.y = 100
    def add_node(self, node):
        self.nodes.append(node)
        print "added node"



    def print_graph(self):
        print "Printing graph in model"
        for n in self.nodes:
            print "Node: ", n
            print n.links, "\n"

        print "\n"

    def calculate_pos(self):
        m = self.x
        n = self.y
        self.x +=100
        self.y+=100
        return (m,n)

    def find_event_handler(self, touch):
        x , y = touch.x, touch.y
        print "in event handler"
        for eachChild in self.nodes:
            node = eachChild.get_ui_reference()
            if node:
                print "in x"
                if node.collide_point(x, y):
                    print " in collision"
                    return eachChild
        return False

class Node():
    def __str__(self):
        return ':\t'.join([self.keyword, self.href])

    def __init__(self, parent, keyword, href, img_src, text, links, has_visited=False):

        self.pos = Model().calculate_pos()
        self.parent = parent #UI NODE not MODEL NODE
        self.keyword = keyword
        self.href = href
        self.img_src = img_src
        self.text = text
        self.links = links
        self.has_visited = has_visited
        self.ui_reference = None

    def get_parent(self):
        return self.parent
    def get_keyword(self):
        return self.keyword
    def get_source(self):
        return self.img_src
    def get_text(self):
        return self.text
    def get_pos(self):
        return self.pos
    def set_id(self, ref):
        print "ref",ref
        if self.parent == None:
            self.parent = ref

        self.ui_reference = ref
    def get_ui_reference(self):
        return self.ui_reference



