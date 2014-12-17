# model.py

import common.singleton as singleton
from random import random
import math
from kivy.clock import Clock

class Model(object):
    __metaclass__ = singleton.Singleton

    def __init__(self, node_creation, edge_creation, **kwargs):
        """
         Creates empty model of nodes and edges, prepares to dispatch when updated
        """
        super(Model, self).__init__(**kwargs)
        self.nodes = []
        self.edges = []
        self.ui_edges = []

        self.node_creation = node_creation
        self.edge_creation = edge_creation


    def add_node(self, node):
        self.nodes.append(node)
    def add_edge(self, edge):
        self.edges.append(edge)


    def find_event_handler(self, touch):
        x , y = touch.x, touch.y
        for eachChild in self.nodes:
            node = eachChild.get_ui_reference() 
            if node:
                if node.collide_point(x, y):
                    return eachChild
        return False

    def has_been_explored_yet(self, keyword):
        for eachNode in self.nodes:
            if keyword==eachNode.get_keyword():
                if eachNode.has_visited == False:
                    return False
                return True
        return False
    def dump_nodes(self):
        self.nodes = []
        self.x = 0
        self.y = 0
    def dump_edges(self):
        self.edges={}
        self.ui_edges = []

    def get_edges(self):
        return self.ui_edges

    def calculate_pos(self, parent_coords):
        center_point = (parent_coords[0], parent_coords[1])
        if len(self.nodes) == 0:
            return center_point
        else:
            # assume we're adding the last item to the list
            current_node = self.nodes[-1]
            count = len(self.nodes)

            ring = (count-1) / 8
            child_dist = 300
            print 'ring:', ring
            if ring > 0:
                child_dist = child_dist / 1.5

            degrees_each = 360/ 8
            radians_each = math.radians(degrees_each)
            rads = radians_each * count
            x_pos = child_dist * math.cos(rads) + center_point[0]
            y_pos = child_dist * math.sin(rads) + center_point[1]
            return (x_pos,y_pos)

class Node(object):

    def __init__(self, parent, keyword, pos=(0,0), has_visited=False):
        self.pos = pos

        self.keyword = keyword
        self.parent = parent #MODEL NODE

        self.ui_reference = None
        self.has_visited = has_visited     

    def get_parent(self):
        return self.parent
    def get_keyword(self):
        return self.keyword
    def get_pos(self):
        return self.get_ui_reference().pos
    def set_id(self, ref):
        # print "ref",ref
        if self.parent == None:
            self.parent = ref
        self.ui_reference = ref
    def get_ui_reference(self):
        return self.ui_reference
    def get_parent_ui_reference(self):
        return self.parent.get_ui_reference()



class WikiPediaPageNode(Node):
    #def __init__(self, parent, keyword, href, img_src, summary, page_content, links, has_visited=False):
    def __init__(self, parent, keyword, href, img_src, summary, pagecontent, links, has_visited):
        super(WikiPediaPageNode, self).__init__(parent, keyword, has_visited=has_visited)
        if parent == None:
            self.pos = Model().calculate_pos((0,0))
        else:
            self.pos = Model().calculate_pos(parent.get_pos())
        self.href = href
        self.img_src = img_src
        self.summary = summary
        self.page_content = pagecontent
        self.links = links # dict -- keyword: url
      


    def get_source(self):
        return self.img_src
    def get_summary(self):
        return self.summary
    def get_pos(self):
        return self.get_ui_reference().pos


