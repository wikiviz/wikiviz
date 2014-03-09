import kivy
kivy.require('1.8.0')

from random import random 
from kivy.app import App
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

    abs_sx = NumericProperty(0)
    abs_sy = NumericProperty(0)

    def __init__(self, **kwargs):
        super(ScatterPlane, self).__init__(**kwargs)
        
        self.do_rotation = False
        self.do_scale = False
        self.do_translation= False
   
     
    def display(self):   
        self.remove_widget(self.uis)
        self.do_scale = True
        self.do_translation= True

        node = NodeWithBkgrd(size=(100,100), pos=(self.center_x-50,self.center_y-50))
        self.add_widget(node)
        node1 = NodeWithBkgrd(size=(100,100), pos=(800,800))
        self.add_widget(node1)
        node.display("http://i1164.photobucket.com/albums/q572/marshill2/sun_zps0fa10dc5.jpg")
        node1.display("http://i1164.photobucket.com/albums/q572/marshill2/sun_zps0fa10dc5.jpg")

        self.connect_with_line(node, node1)

    def connect_with_line(self,node1, node2):
        with self.canvas:
            Color = (random(),random(),random())
            Line(points = [node1.center_x,node1.center_y,node2.center_x,node2.center_y], width=2)
        self.remove_widget(node1)
        self.remove_widget(node2)
        self.add_widget(node1)
        self.add_widget(node2)


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
        if (abs(touch.x - self.center_x) <=(self.width) and abs(touch.y - self.center_y) <= (self.height)):
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


class UISearchButton(Button):

    def on_touch_down(self,touch):
        if (abs(touch.x - self.center_x) <=self.width/2 and abs(touch.y - self.center_y) <= self.width/2):
            uis = self.parent
            uic = uis.parent
            uic.display()
        return



class WikiVizApp(App):
    



    def build(self):
        
        bkgrd = UIC()       
       
        return bkgrd


if __name__=='__main__':
    WikiVizApp().run()
        
