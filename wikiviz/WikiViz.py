import kivy
kivy.require('1.8.0')

from random import random 
from math import sqrt
from math import cos
from math import sin
from math import atan2
from math import degrees
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.uix.scatter import ScatterPlane, Scatter
from kivy.uix.pagelayout import PageLayout
from kivy.uix.image import Image
from kivy.uix.image import AsyncImage
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty, StringProperty, NumericProperty, ListProperty, BooleanProperty
from kivy.graphics import Line, Color
from kivy.graphics.transformation import Matrix
from kivy.graphics.stencil_instructions import StencilPush, StencilPop, StencilUse
from kivy.animation import Animation
from kivy.core import window



#TODO LIST: ERROR WHEN YOU CLICK NO!!!!!





'''
                                NODE CLASSES
'''

class Node(Scatter):
    image = ObjectProperty(None)
    label = ObjectProperty(None)

    move = NumericProperty(0)
    flag = NumericProperty(0)

    def __init_(self, **kwargs):
        
        super(Node, self).__init__(kwargs)
        self.do_rotation = False
        self.do_scale = False
        self.do_translation = False
        self.flag = 0

    def display(self, link):
        self.image.source = link
        return
    def on_touch_up(self, touch):
        print "TOUCH NODE UP", touch.x, touch.y
        
        if (self.collide_point(touch.x, touch.y)):

            self.parent.parent.page= 1
            self.parent.parent.do_layout()
            self.parent.parent.summary.text = "INSERT SUMMARY HERE"
            self.parent.parent.uic.disabled = True

        return super(Node, self).on_touch_up(touch)


    def on_touch_move(self, touch):
        
        return super(Node, self).on_touch_move(touch)


    def on_touch_down(self, touch):
        
        return super(Node, self).on_touch_down(touch)
 
        

     
'''
                            END NODE CLASSES
''' 

class Edge(Widget):
    theta = NumericProperty(0)
    p = ObjectProperty(None)
    c = ObjectProperty(None)  

    def __init__(self,parent, child, **kwargs):
        self.p = parent
        self.c = child

        super(Edge, self).__init__(**kwargs)
      
        #self.height = 20
        #self.center_x, self.center_y = parent.center_x, parent.center_y
        #self.rotation = degrees(atan2((parent.y-child.y), (parent.x-child.x)))
        #self.rotation = degrees(atan2((parent.y-child.y), (parent.x-child.x)))
        #print "parent = ", parent.center_x

        print self.pos
        #self.height = 20
        #self.width = self.find_width()
       
    def _get_p(self):
        return self.p
    def _get_c(self):
        return self.c

    def find_width(self):
        x = self.p.x-self.c.x
        y = self.p.y-self.c.y
        return sqrt(x*x + y*y)


    def on_touch_down(self, touch):
        print touch
    def on_touch_up(self, touch):
        print touch
    def on_touch_move(self, touch):
        print touch





class UIC(ScatterPlane):

    obj = ListProperty(None)

    is_popup_displayed = BooleanProperty(False)

    def __init__(self, **kwargs):



        super(UIC, self).__init__(**kwargs)
        

        self.do_rotation = False
        self.do_scale = False
        self.do_translation= False


       

        return
     
    def display(self):   
        self.uis.disabled= True
        keyword= self.uis.search_bar.text 
        self.remove_widget(self.uis)
 
        self.uibc.disabled= False

        self.do_scale = True
        self.do_translation= True
   

        '''
                    This code will be deleted when model is hoooked up
        '''
        
        node = Node(size=(100,100), pos=(0,0))
        node.label.text = self.uis.search_bar.text
        self.add_widget(node)
        node1 = Node(size=(100,100), pos=(300,500))
        self.add_widget(node1)
        node.display("http://i1164.photobucket.com/albums/q572/marshill2/sun_zps0fa10dc5.jpg")
        node1.display("http://i1164.photobucket.com/albums/q572/marshill2/sun_zps0fa10dc5.jpg")
        x = Edge(node,node1)
        self.add_edge(x)

        '''
                            END DELETEION
        '''
        self.add_widget(self.uibc)

      
        return



    def add_node(self, *args):
        if len(args) == 1:
            model_node = args[0]
        elif len(args) == 2:
            model_node = args[1]
        source=model_node.get_source() 
        keyword = model_node.keyword
        pos = model_node.get_pos()

        to_be_added = Node(pos = pos)
        to_be_added.display(source)
        to_be_added.label.text= keyword
        self.add_widget(to_be_added)

    def add_edge(self, edge):
        self.add_widget(edge)
        return

    def confirm_new_search(self):

        self.add_widget(self.uipup)
        self.do_translation = False
        self.is_popup_displayed = True

    def decline_new_search(self):
        self.remove_widget(self.uipup)
        self.do_translation = True
        self.is_popup_displayed = False

    def new_search(self):

        self.scale = 1.0
        self.do_translation = True
        self.remove_widget(self.uibc)
        self.remove_widget(self.uis)
        self.remove_widget(self.uipup)
        self.is_popup_displayed = False
        self.clear_widgets()
        self.pos = (0,0)
        self.add_widget(self.uis)

        self.uis.disabled = False
        self.uibc.disabled= True

        self.uis.search_bar.font_size = self.uis.height - 20
        self.uis.search_bar.font_name = 'DroidSans'

        self.do_scale = False
        self.do_translation= False

        self.uis.search_bar.text  = 'Search a Word'

        return

 
    def remove_widget(self, to_remove):
        super(UIC, self).remove_widget(to_remove)
        return 0
    def on_touch_down(self, touch):
        if self.is_popup_displayed:
            return False
        x, y = touch.x, touch.y     
        if not self.do_collide_after_children:
            if not self.collide_point(x, y):
                return False
        touch.push()
        touch.apply_transform_2d(self.to_local)
        for eachChild in self.children:
            if eachChild.collide_point(touch.x, touch.y):
                eachChild.on_touch_down(touch)
                touch.pop()
                self._bring_to_front()
                return True

        touch.pop()
        if not self.do_translation_x and \
                not self.do_translation_y and \
                not self.do_rotation and \
                not self.do_scale:
            return False

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
            if super(Scatter, self).on_touch_move(touch):
                touch.pop()
                return True
            touch.pop()
        if touch in self._touches and touch.grab_current == self:
            if self.transform_with_touch(touch):
                self.dispatch('on_transform_with_touch', touch)
            self._last_touch_pos[touch] = touch.pos
        if self.collide_point(x, y):
            return True
    def on_touch_up(self, touch):
        if self.is_popup_displayed:
            touch.x, touch.y = self.to_local(touch.x,touch.y)
            if self.uipup.collide_point( touch.x, touch.y ):
                print " COLLISION"
                self.uipup.on_touch_up(touch)
                return True
            return False
        x, y = touch.x, touch.y
        if not touch.grab_current == self:
            touch.push()
            touch.apply_transform_2d(self.to_local)
            if super(Scatter, self).on_touch_up(touch):
                touch.pop()
                return True
            touch.pop()
        if touch in self._touches and touch.grab_state:
            touch.ungrab(self)
            del self._last_touch_pos[touch]
            self._touches.remove(touch)
        if self.collide_point(x, y):
            return True



            


class Scatter_Summary_Widget(PageLayout):
    uic = ObjectProperty(None)
    summary = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Scatter_Summary_Widget, self).__init__(**kwargs)
        self.uic.remove_widget(self.uic.uipup)
        self.uic.remove_widget(self.uic.uibc)
########################## OVERRIDE FUNCTIONS##############################################
    def do_layout(self, *largs):
        l_children = len(self.children)
        for i, c in enumerate(reversed(self.children)):
            if i < l_children:
                width = self.width - self.border
            else:
                width = self.width - 2 * self.border

            if i == 0:
                self.uic.diabled = False
                x = self.x

            elif i < self.page:
                x = self.x

            elif i == self.page:
                x = self.x + self.border

            elif i == self.page + 1:
                x = self.right - self.border

            else:
                x = self.right

            c.height = self.height
            c.width = width       
            if i != 0:
                Animation(
                    x=x,
                    y=self.y,
                    d=.5, t='in_quad').start(c)

    def on_touch_down(self, touch):
        return self.children[self.page - 1].on_touch_down(touch)

    def on_touch_move(self, touch):
        return self.children[self.page - 1].on_touch_move(touch)

    def on_touch_up(self, touch):
        return self.children[self.page-1].on_touch_up(touch)
############################################################################################
    
class UISummary(ScrollView):

    text = StringProperty(None)
########################### OVERRIDE FUNCTIONS #############################################
    def on_touch_down(self, touch):
        print "here down"
        return 

    def on_touch_up(self, touch):
        print "here up"
        self.parent.uic.disabled = False
        self.parent.page -= 1
        return
############################################################################################
        

class gr(ScatterPlane):
    container = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(gr, self).__init__(**kwargs)
        self.do_rotation = False
        self.obj = None
        self.zoom_or_not = 0

    def on_touch_down(self, touch):
        x, y = touch.x, touch.y     
        if not self.do_collide_after_children:
            if not self.collide_point(x, y):
                return False
        touch.push()
        touch.apply_transform_2d(self.to_local)
        if super(Scatter, self).on_touch_down(touch):
            touch.pop()
            self._bring_to_front()
            return True
        touch.pop()
        if not self.do_translation_x and \
                not self.do_translation_y and \
                not self.do_rotation and \
                not self.do_scale:
            return False

        if self.do_collide_after_children:
            if not self.collide_point(x, y):
                return False
        self._bring_to_front()
        touch.grab(self)
        self._touches.append(touch)
        self._last_touch_pos[touch] = touch.pos

        return True

    def on_touch_move(self, touch):
        x, y = touch.x, touch.y
        if self.collide_point(x, y) and not touch.grab_current == self:
            touch.push()
            touch.apply_transform_2d(self.to_local)
            if super(Scatter, self).on_touch_move(touch):
                touch.pop()
                return True
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
            if super(Scatter, self).on_touch_up(touch):
                touch.pop()
                return True
            touch.pop()
        if touch in self._touches and touch.grab_state:
            touch.ungrab(self)
            del self._last_touch_pos[touch]
            self._touches.remove(touch)
        if self.collide_point(x, y):
            return True

class sc(Scatter):
    image = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(sc, self).__init__(**kwargs)
        self.move_or_not = 0

    def on_touch_move(self, touch):
        #print "MOVE"

        return super(sc, self).on_touch_move(touch)
    def on_touch_up(self, touch):
        #print "UP"
 
        return super(sc, self).on_touch_up(touch)

    def on_touch_down(self, touch):
        print touch.x, touch.y

        return super(sc, self).on_touch_down(touch)

    def clicked_me(self, touch):
        if (self.collide_point(touch.x, touch.y)):
            print "CLICKED ME"
            return True
        return False

class WikiVizApp(App):

    bkgrd = ObjectProperty(None)


    def build(self):
        bkgrd= Scatter_Summary_Widget()
#        bkgrd = gr()
#        for i in range(0, 10):
#            x = sc(pos = (i*100,i*100))
#            x.image.source = "http://i1164.photobucket.com/albums/q572/marshill2/sun_zps0fa10dc5.jpg"
#            bkgrd.add_widget(x)
            #x.pos = (i*100,i*100)

        #bkgrd.uic.add_widget(x)
        return bkgrd

if __name__=='__main__':
    WikiVizApp().run()
        
