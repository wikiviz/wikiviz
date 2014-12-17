from kivy.uix.scatter import ScatterPlane
from kivy.properties import ObjectProperty,BooleanProperty
from kivy.clock import Clock

from ui_classes.searchbar import SearchBar

class UIContainer(ScatterPlane):
    '''
    Modified ScatterPlane layout
    Contains Nodes and Edges and Controller
    '''
    is_popup_displayed = BooleanProperty(False)
    blocked = BooleanProperty(False)
    controller = ObjectProperty(None)
    uis = ObjectProperty(None)
    background = ObjectProperty(None)
    def __init__(self,controller, node, edge, **kwargs):
        super(UIContainer, self).__init__(**kwargs)
        # rotation and scale controls

        self.do_rotation = False
        self.do_scale = False
        self.do_translation= False
        self.scale_max = 100.0
        self.scale_min = .01
        # register event
        self.register_event_type("on_add_node")
        self.register_event_type("on_initialize")

        Clock.schedule_once(self.on_initialize)
        # reference to Controller, with callback function
        self.controller = controller(self.on_add_node, self.add_red_edge, self.add_edge)
        self.Node = node
        self.Edge = edge
    
        
        return
    def on_initialize(self, *args):
        self.uis = SearchBar(self.initial_search, pos = (100, 100))
        self.add_widget(self.uis)


    def initial_search(self, *args):
        ''' Called once for the initial search
            Pulls keyword from search bar text
        '''
        self.pos = (self.width/2,self.height/2)
        self.remove_widget(self.uis)
        self.do_scale = True
        self.do_translation= True  
        self.controller.search_by_keyword(None, self.uis.search_bar.text)

        return
    #
    # TOUCH FUNCTIONS
    #

    def on_touch_down(self, touch):
        '''
        Determine action on touch based on current state
        '''
 
        # do nothing if popup displayed
        if self.is_popup_displayed:
            return False
  
        # do nothing if touch causes children to exceed screen bounds (?)
        x, y = touch.x, touch.y
        if not self.do_collide_after_children:
            if not self.collide_point(x, y):
                return False

        # otherwise respond to touch
        touch.push()
        touch.apply_transform_2d(self.to_local)
 
        # do nothing if controller is already handling the event (?)
        if self.controller.find_event_handler(touch, 'on_touch_down'):
            touch.pop()
            return False

        if self.uis.collide_point(x,y):
            self.uis.on_touch_down(touch)
            touch.pop()
            return False

  

        touch.pop()


        if self.do_collide_after_children:
            if not self.collide_point(x, y):
                return False

        self._bring_to_front()
        touch.grab(self)
        self._touches.append(touch)
        self._last_touch_pos[touch] = touch.pos

        return True


    def on_touch_move(self, touch):
        if self.is_popup_displayed:
            return False
        x, y = touch.x, touch.y
        if self.collide_point(x, y) and not touch.grab_current == self:
            touch.push()
            touch.apply_transform_2d(self.to_local)
            if self.controller.find_event_handler(touch, 'on_touch_move'):
                touch.pop()
                return False
            if self.uis.collide_point(x,y):
                self.uis.on_touch_move(touch)
                touch.pop()
                return False
            touch.pop()
        if touch in self._touches and touch.grab_current == self:
            if self.transform_with_touch(touch):
                self.dispatch('on_transform_with_touch', touch)
            self._last_touch_pos[touch] = touch.pos
        if self.collide_point(x, y):
            return True


    def on_touch_up(self, touch):
        x, y = touch.x, touch.y
        if self.is_popup_displayed:
            return False

        if not touch.grab_current == self:
            touch.push()
            touch.apply_transform_2d(self.to_local)
            if self.controller.find_event_handler(touch, 'on_touch_up'):
                touch.pop()
                return False
            if self.uis.collide_point(x,y):
                self.uis.on_touch_up(touch)
                touch.pop()
                return False

            touch.pop()
        if touch in self._touches:
            touch.ungrab(self)
            del self._last_touch_pos[touch]
            self._touches.remove(touch)
        if self.collide_point(x, y):
            return True


    #
    # FUNCTIONS CALLED BY EVENTS
    #


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
        to_be_added._bring_to_front()
        parent._bring_to_front()
        return edge
     

    def add_red_edge(self, child_model_node):
        child_ui = child_model_node.get_ui_reference()
        parent_ui = child_model_node.get_parent().get_ui_reference()
        try:
            parent_ui.edges[child_ui].change_color(1,0,0)
        except KeyError:
            return

    def dump_nodes(self):
        self.controller.dump_nodes()
        self.children = []
    def dump_edges(self):
        for eachEdge in self.controller.get_edges():
            self.remove_widget(eachEdge)
        self.controller.dump_edges()

  