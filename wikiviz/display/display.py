import kivy
kivy.require('1.0.7')

from kivy.app import App
from kivy.uix.scatter import ScatterPlane
from kivy.uix.image import Image
from kivy.uix.image import AsyncImage
from kivy.uix.widget import Widget
from kivy.uix.stencilview import StencilView
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics.vertex_instructions import BorderImage, Ellipse
from kivy.graphics.stencil_instructions import *
from kivy.graphics import Color
from kivy.properties import ObjectProperty, NumericProperty
from os.path import join
from functools import partial


class UIContainer(ScatterPlane):
    go = ObjectProperty(None)
    searchbox = ObjectProperty(None)
    share = ObjectProperty(None)


    def add_node(self, node1):
        self.add_widget(node1)
        return
        

class Node(StencilView):

    modelimage = ObjectProperty(None)
 
  
    def display_image(self, link):
        self.modelimage.source = link
        self.modelimage.size = (5000,5000)
        
        return 

class Stencil(Widget):
    modelimage = ObjectProperty(None)
    stack_num = NumericProperty(0)
    def display(self, link):
        if self.stack_num==1:
            self.stack_num = 0
            StencilPop()
        self.modelimage.source = link
        self.modelimage.size = (500,500)
        StencilPush()
        StencilUse()
        self.stack_num =1
        return





class DisplayApp(App):
    def build(self):
        gr = Stencil(pos = (0,0), size = (1750,1750))

        background1 = UIContainer()
        node1 = Node(size= (2000,2000), pos = (0,0))
        node1.display_image("http://i1164.photobucket.com/albums/q572/marshill2/sun_zps0fa10dc5.jpg")
        gr.display("http://i1164.photobucket.com/albums/q572/marshill2/sun_zps0fa10dc5.jpg")
        #background1.add_node(node1)
        background1.add_node(gr)
   
        return background1



if __name__ == '__main__':
    DisplayApp().run()
