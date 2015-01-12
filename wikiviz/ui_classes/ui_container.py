from kivy.uix.scatter import ScatterPlane
from kivy.properties import ObjectProperty,BooleanProperty
from kivy.clock import Clock
from ui_classes.node import NodeContainer
from ui_classes.searchbar import SearchBar
from ui_classes.controls import ControlsLayout, ResetSearchPopup
from kivy.core import window
from kivy.uix.widget import Widget
from ui_classes.summarybox import UISummary

class UIContainer(Widget):
    ui_scatter = ObjectProperty(None)
    controls = ObjectProperty(None)
    reset_popup= ObjectProperty(None)
    ui_summary = ObjectProperty(None)
    def __init__(self,controller, node, edge, **kwargs):
        print "INIT"
        super(UIContainer, self).__init__(**kwargs)
        self.register_event_type("on_initialize")
        Clock.schedule_once(self.on_initialize)
        self.controller = controller
        self.node = node
        self.edge = edge
    def on_initialize(self, *args):
        print "On INIT"
        self.ui_scatter = WikiUIScatter(self.controller, self.node,self.edge, self.add_controls, self.add_summary)
        self.add_widget(self.ui_scatter)

    def add_controls(self):
        self.controls = ControlsLayout(self.reset_choice)
        self.add_widget(self.controls)

    def add_summary(self, title, text):
        self.ui_summary = UISummary(title, text,self.remove_summary)
        self.add_widget(self.ui_summary)
        return
    def remove_summary(self):
        self.remove_widget(self.ui_summary)

    def reset_choice(self):
        self.remove_widget(self.controls)
        self.reset_popup = ResetSearchPopup(self.reset_search, self.remove_reset_popup)
        self.add_widget(self.reset_popup)

    def remove_reset_popup(self):
        self.remove_widget(self.ui_scatter)
        self.remove_widget(self.reset_popup)
        self.add_widget(self.ui_scatter)
        self.add_widget(self.controls)

    def reset_search(self):
        self.dump_graph()
    def dump_graph(self):
        print "Dump Graph"
        self.remove_widget(self.ui_scatter)
        self.on_initialize()


class UIScatter(ScatterPlane):
    '''
    Modified ScatterPlane layout
    Contains Nodes and Edges and Controller
    '''

    background = ObjectProperty(None)

    def __init__(self, **kwargs):
        print "Init Scatter"
        super(UIScatter, self).__init__(**kwargs)
        # rotation and scale controls

        self.do_rotation = False
        self.do_scale = False
        self.do_translation= False
        self.scale_max = 100.0
        self.scale_min = .01
        # register event
        self.register_event_type("on_initialize")
        Clock.schedule_once(self.on_initialize)
        # reference to Controller, with callback function
     
        return

    def on_initialize(self, *args):
        print "On Init base"
        pass

    #
    # TOUCH FUNCTIONS
    #

    def on_touch_down(self, touch):
        '''
        Determine action on touch based on current state
        '''
 
  
        # do nothing if touch causes children to exceed screen bounds (?)
        x, y = touch.x, touch.y
        if not self.do_collide_after_children:
            if not self.collide_point(x, y):
                return False

        # otherwise respond to touch
        touch.push()
        touch.apply_transform_2d(self.to_local)
 
        # do nothing if controller is already handling the event (?)

        for eachChild in self.children:

            if eachChild.on_touch_down(touch):
                touch.pop()
                return False

        touch.pop()
 

        if self.do_collide_after_children:
            if not self.collide_point(x, y):
                return False

        #self._bring_to_front()
        touch.grab(self)
        self._touches.append(touch)
        self._last_touch_pos[touch] = touch.pos
        return True


    def on_touch_move(self, touch):
        x, y = touch.x, touch.y
        if self.collide_point(x, y) and not touch.grab_current == self:
            touch.push()
            touch.apply_transform_2d(self.to_local)
            for eachChild in self.children:
                if eachChild.on_touch_move(touch):
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

        if not touch.grab_current == self:
            touch.push()
            touch.apply_transform_2d(self.to_local)
            for eachChild in self.children:
                if eachChild.on_touch_up(touch):
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

  
class WikiUIScatter(UIScatter):
    uis = ObjectProperty(None)
    new_search_button = ObjectProperty(None)
    node_container = ObjectProperty(None)
    def __init__(self,controller, node, edge, add_controls, add_summary,  **kwargs):
        print "Init WikiScatter"
        super(WikiUIScatter, self).__init__(**kwargs)
        # rotation and scale controls
        # reference to Controller, with callback function
        self.node_container = NodeContainer(controller,node,edge, add_summary)
        self.add_controls = add_controls      
        return
    def on_initialize(self, *args):
        print "On Init WikiScatter"
        self.uis = SearchBar(self.initial_search, pos = (100, 100))
        self.add_widget(self.uis)
    def initial_search(self, *args):
        ''' Called once for the initial search
            Pulls keyword from search bar text
        '''
        print "Search"
        print args
        self.pos = (self.width/2,self.height/2)
        self.remove_widget(self.uis)
        self.do_scale = True
        self.do_translation= True  
        self.node_container.search_by_keyword(*args)
        self.add_widget(self.node_container)
        self.add_controls()
        return
    def reset_search(self):
        self.remove_widget(self.new_search_button)
        self.dump_graph()
    def dump_graph(self):
        print "Dump Graph"
        self.controller.dump_nodes()
        self.clear_widgets(self.children)
        self.controller.dump_edges()