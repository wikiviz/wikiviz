from kivy.properties import ObjectProperty, StringProperty, DictProperty, NumericProperty
from kivy.uix.scatter import Scatter
from kivy.uix.widget import Widget
from kivy.graphics import Color
from random import random
from kivy.clock import Clock

class NodeContainer(Widget):
    controller = ObjectProperty(None)
    def __init__(self,controller, node, edge, *args, **kwargs):
        super(NodeContainer, self).__init__(**kwargs)
        self.register_event_type("on_add_node")
        self.controller = controller(self.on_add_node, self.add_red_edge, self.add_edge, *args)
        self.Node = node
        self.Edge = edge

    def search_by_keyword(self, keyword):
        print keyword
        self.controller.search_by_keyword(None,keyword)

    def on_touch_down(self,touch):
        if self.controller.find_event_handler(touch, 'on_touch_down'):
            return True
    def on_touch_move(self, touch):
        if self.controller.find_event_handler(touch, 'on_touch_move'):
            return True
    def on_touch_up(self,touch):
        if self.controller.find_event_handler(touch, 'on_touch_up'):
            return True

    def on_add_node(self, model_node, *args):
        ''' Callback function. Called when network returns with model data.
         @param Model Node reference
        '''

        # retrieve data from model node
        source = model_node.get_source()
        keyword = model_node.get_keyword()
        pos = model_node.get_pos()

        # create new UI Node
        
        to_be_added = self.Node(pos=pos)
        
        model_node.set_id(to_be_added) #set model_node's reference to UI node

 
        # change image to format we need in UI
        # images is stored as a list; we just want the first one
        if len(source) == 0:
            source = ''
        else:
            source = source[0]

        to_be_added.source = source
        to_be_added.keyword = keyword

        # add UI Node and Edge to the screen
        self.add_widget(to_be_added)

 

    def add_edge(self,parent, to_be_added):

        edge =  self.Edge(parent, to_be_added)
        self.add_widget(edge) # parent, child
        #to_be_added._bring_to_front()
        #parent._bring_to_front()
        return edge
     

    def add_red_edge(self, child_model_node):
        child_ui = child_model_node.get_ui_reference()
        parent_ui = child_model_node.get_parent().get_ui_reference()
        try:
            parent_ui.edges[child_ui].change_color(1,0,0)
        except KeyError:
            return


class UINode(Scatter):
    '''
    @class Node
    UI Node. Represents a vertex in the graph, with ref to model node for data.
    '''
    
    label = ObjectProperty(None)
    circle = ObjectProperty(None)
    keyword = StringProperty(None)
    edges = DictProperty(None)
    move = NumericProperty(0)
 

    def __init__(self, **kwargs):
        ''' Set initial scale and rotation controls
        '''

        super(UINode, self).__init__(**kwargs)

        self.do_rotation = False
        self.do_scale = True
        self.do_translation = True
        self.scale_min = .5
        self.scale_max = 2.5

        #self.circle.canvas.children[0] = Color(random(),random(),random())



        

    def collide_point(self, x, y):
        ''' Determine whether a point is within the safe area of the screen (?)
        '''
        x, y = self.to_local(x, y)
        return -1.1*self.width/8 <= x <= 1.2*self.width and -1.1*self.height/8 <= y <= 1.2*self.height


    def on_touch_up(self, touch):
        ''' Determine whether touch is intending to move or tap the node
            then call appropriate event
        '''
        if touch in self._touches:
            touch.ungrab(self)
            del self._last_touch_pos[touch]
            self._touches.remove(touch)
        return True


    def on_touch_move(self, touch):
        ''' Move the node along with the touch
        '''
        x, y = touch.x, touch.y
        if touch in self._touches and touch.grab_current == self:
            self.move+=1
            if self.transform_with_touch(touch):
                self.dispatch('on_transform_with_touch', touch)
            self._last_touch_pos[touch] = touch.pos
        return True


    def on_touch_down(self, touch):
        ''' record initial touch for later processing
        '''
        self.move = 0
        x, y = touch.x, touch.y
        #self._bring_to_front()
        if self._touches != []:
            return True
        touch.grab(self)
        self._touches.append(touch)
        self._last_touch_pos[touch] = touch.pos
        return True


    def display(self, link):
        ''' Set Node's image source to the link parameter
         @param The link to use as the node's image source
        '''
        self.image.source = link
        return

class WikiPediaUINode(UINode):
    image = ObjectProperty(None)
    source = StringProperty(None)
    def __init__(self, **kwargs):
        super(WikiPediaUINode, self).__init__(**kwargs)
        self.label.pos = (self.image.x, self.image.y+self.image.height)

    def user_wants_summary(self):
        ''' Determine whether to user intends to get summary
            based on distance travelled
            @returns bool
        '''
        if self.move < 10:
            return True
        return False