from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget
from kivy.graphics import Color
class Edge(Widget):
    ''' @class Edge
        Represents a connection between Nodes.
        Draws a line between vertices.
    '''
    p = ObjectProperty(None)
    c = ObjectProperty(None)  

    def __init__(self, parent, child, **kwargs):
        '''
        @param parent Reference to parent Node object
        @param child Reference to child Node object
        '''
        self.p = parent
        self.c = child

        super(Edge, self).__init__(**kwargs)
        parent.edges[child] = self


    def change_color(self, r, g, b):
        self.canvas.children[1] = Color(r,g,b)

    def collide_point(self, x, y):
        return False
    def on_touch_down(self, touch):
        return
    def on_touch_up(self, touch):
        return
    def on_touch_move(self, touch):
        return


