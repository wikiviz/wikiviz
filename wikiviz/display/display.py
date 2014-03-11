import kivy
kivy.require('1.8.0')

from random import random 
from kivy.app import App
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.uix.scatter import ScatterPlane
from kivy.uix.image import Image
from kivy.uix.image import AsyncImage
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty, NumericProperty, ListProperty, ReferenceListProperty
from kivy.graphics import *
from kivy.graphics.stencil_instructions import StencilPush, StencilPop, StencilUse





class UIC(ScatterPlane):
    uis = ObjectProperty(None)
    uibc = ObjectProperty(None)

    Nodes = ListProperty(None)


    abs_l = NumericProperty(0)
    abs_h = NumericProperty(0)



    def __init__(self, **kwargs):
        super(ScatterPlane, self).__init__(**kwargs)
        


        
        self.uibc.disabled = True
        self.uibc.opacity = 0
  
  

        self.do_rotation = False
        self.do_scale = False
        self.do_translation= False
        
   
     
    def display(self):   
        print " KEYWORD=", self.uis.search_bar.text 
        self.uis.opacity = 0
        self.uis.disabled= True
        
        self.uibc.opacity = 100
        self.uibc.disabled= False

        self.do_scale = True
        self.do_translation= True

        node = NodeWithBkgrd(size=(100,100), pos=(0,0))
        self.add_widget(node)
        node1 = NodeWithBkgrd(size=(100,100), pos=(800,800))
        self.add_widget(node1)
        node.display("http://i1164.photobucket.com/albums/q572/marshill2/sun_zps0fa10dc5.jpg")
        node1.display("http://i1164.photobucket.com/albums/q572/marshill2/sun_zps0fa10dc5.jpg")
        self.connect_with_line((0,0), (800,800))

    def add_node(self, node):
        self.add_widget(node)
    def connect_with_line(self,coord1, coord2):
        with self.canvas:
            Color = (random(),random(),random())
            Line(points = [coord1[0], coord1[1], coord2[0], coord2[1]], width=2)

    def new_search(self):
        self.scale = 1.0
       
  
        self.remove_widget(self.uibc)
        self.remove_widget(self.uis)
        self.canvas.clear()
        self.pos = (0,0)

 
        self.add_widget(self.uibc)
        self.add_widget(self.uis)
       
        self.uis.opacity = 100
        self.uis.disabled = False
        self.uibc.opacity = 0
        self.uibc.disabled= True
        self.do_scale = False
        self.do_translation= False

    def on_transform_with_touch(self, touch):
        return

    def on_touch_down(self, touch):
        print "scale =" , self.scale
        print " touch down"
        super(ScatterPlane, self).on_touch_down(touch)
        return
    def on_touch_move(self, touch):
        print "scale =" , self.scale
        print "on touch move"
        print touch
        super(ScatterPlane, self).on_touch_move(touch)
        return
    def on_touch_up(self, touch):
        print " touch up"
        super(ScatterPlane, self).on_touch_up(touch)
        return


class NodeWithBkgrd(Widget):
    node = ObjectProperty(None)
    def display(self, link):
        self.node.display(link)
        self.node.pos = self.pos
        return
    def on_touch_down(self, touch):
        print self.pos[0], self.pos[1]
        if (abs(touch.x - self.pos[0]) <=2*(self.width) and abs(touch.y - self.pos[1]) <= 2*(self.height)):
            print "here"
        return


class Node(AsyncImage):


    def display(self, link):
        self.source= link      
        return
        

    
    
class UISearch(Widget):
    search_bar = ObjectProperty(None)
    go_button = ObjectProperty(None)


class UITextInput(TextInput):


    def on_touch_up(self, touch):
        self.text = ''
        super(TextInput, self).on_touch_up(touch)
        return


class UISearchButton(Image, ButtonBehavior):

    def on_touch_down(self,touch):
        if (abs(touch.x - self.center_x) <=self.width/2 and abs(touch.y - self.center_y) <= self.width/2):
            uis = self.parent
            uic = uis.parent
            uic.display()
        return

class UINSearchButton(Image, ButtonBehavior):
    def on_touch_down(self,touch):
        if (abs(touch.x - self.center_x) <=self.width/2 and abs(touch.y - self.center_y) <= self.width/2):
            uis = self.parent
            uic = uis.parent
            uic.new_search()
            
        return

class UIShare(Image, ButtonBehavior):
    def on_touch_down(self,touch):
        if (abs(touch.x - self.center_x) <=self.width/2 and abs(touch.y - self.center_y) <= self.width/2):
            uis = self.parent
            uic = uis.parent  
            
        return

class UIBContainer(BoxLayout):
    new_search = ObjectProperty(None)
    share = ObjectProperty(None)

    window_c_x = NumericProperty(0)
    window_c_y = NumericProperty(0)



    def upper_left(self, w , h, s):

        parent = self.parent

        w_pos = self.to_window(self.x, self.y)

        self.pos = self.x + (self.window_c_x - w_pos[0])/s, self.y+(self.window_c_y - w_pos[1])/s
        parent.remove_widget(self)
        parent.add_widget(self)


class DisplayApp(App):


    def build(self):
        bkgrd = UIC()
 
       
        return bkgrd


if __name__=='__main__':
    DisplayApp().run()
        
