from kivy.properties import ObjectProperty, StringProperty, DictProperty, NumericProperty
from kivy.uix.scatter import Scatter
from kivy.uix.widget import Widget
from kivy.graphics import Color
from random import random
from kivy.clock import Clock



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

        self.circle.canvas.children[0] = Color(random(),random(),random())



        

    def collide_point(self, x, y):
        ''' Determine whether a point is within the safe area of the screen (?)
        '''
        x, y = self.to_local(x, y)
        return -1.1*self.width/8 <= x <= 1.2*self.width and -1.1*self.height/8 <= y <= 1.2*self.height


    def on_touch_up(self, touch, *args):
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
        self._bring_to_front()
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