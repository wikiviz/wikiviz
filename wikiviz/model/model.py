# model.py
from kivy.event import EventDispatcher
import common.singleton as singleton
from kivy.core.window import Window
from random import random
import math



class Model(EventDispatcher):
    __metaclass__ = singleton.Singleton

    def __init__(self, **kwargs):
        """
         Creates empty model of nodes and edges, prepares to dispatch when updated
        """
        super(Model, self).__init__(**kwargs)
        self.nodes = []
        self.children_per_node = 5
        self.distance_to_child = 200


    def add_node(self, node):
        self.nodes.append(node)
        print "added node"


    def calculate_pos(self):
        center_point = (Window.width/2 - 50, Window.height/2 - 50)
        if len(self.nodes) == 0:
            return center_point
        else:
            # assume we're adding the last item to the list
            current_node = self.nodes[-1]
            count = len(self.nodes)
            degrees_each = 360/self.children_per_node
            radians_each = math.radians(degrees_each)
            rads = radians_each * count
            x_pos = self.distance_to_child * math.cos(rads) + center_point[0]
            y_pos = self.distance_to_child * math.sin(rads) + center_point[1]
            return (x_pos,y_pos)

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

class Node:

    def __init__(self, parent, keyword, href, img_src, summary, pagecontent, links, has_visited=False):

        self.pos = Model().calculate_pos()
        self.parent = parent #MODEL NODE
        self.keyword = keyword
        self.href = href
        self.img_src = img_src
        self.summary = summary
        self.page_content = pagecontent
        self.links = links
        self.has_visited = has_visited
        self.ui_reference = None        

    def get_parent(self):
        return self.parent
    def get_keyword(self):
        return self.keyword
    def get_source(self):
        return self.img_src
    def get_summary(self):
        return self.summary
    def get_pos(self):
        return self.pos
    def set_id(self, ref):
        print "ref",ref
        if self.parent == None:
            self.parent = ref

        self.ui_reference = ref
    def get_ui_reference(self):
        return self.ui_reference
    def get_parent_ui_reference(self):
        return self.parent.get_ui_reference()



