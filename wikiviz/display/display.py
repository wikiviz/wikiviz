import kivy
kivy.require('1.8.0')

from random import random 
from kivy.app import App
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
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

    uipup = ObjectProperty(None)



    def __init__(self, **kwargs):
        self.register_event_type('on_add_node')
        super(ScatterPlane, self).__init__(**kwargs)
        
        
        self.uibc.disabled = True


        self.do_rotation = False
        self.do_scale = False
        self.do_translation= False


        self.remove_widget(self.uibc)
        self.remove_widget(self.uipup)

        

        return

   
     
    def display(self):   
        print " KEYWORD=", self.uis.search_bar.text 
        self.remove_widget(self.uis)
 
        self.uibc.disabled= False

        self.do_scale = True
        self.do_translation= True
        self.uis.disabled= True


        self.add_widget(self.uibc)
        


        '''
                    This code will be deleted when model is hoooked up
        '''
        node = Node(size=(100,100), pos=(0,0))
        self.add_widget(node)
        node1 = Node(size=(100,100), pos=(800,800))
        self.add_widget(node1)
        node.display("http://i1164.photobucket.com/albums/q572/marshill2/sun_zps0fa10dc5.jpg")
        node1.display("http://i1164.photobucket.com/albums/q572/marshill2/sun_zps0fa10dc5.jpg")
        self.connect_with_line((0,0), (800,800))

        '''
                            END DELETEION
        '''


    def on_add_node(self, model_node):
        to_be_added = NodeWithBkgrd(model_node.get_pos())
        to_be_added.display(model_node.get_source())
        self.add_widget(node)

    def connect_with_line(self,coord1, coord2):
        with self.canvas:
            Color = (random(),random(),random())
            Line(points = [coord1[0], coord1[1], coord2[0], coord2[1]], width=2)

    def confirm_new_search(self):
        self.add_widget(self.uipup)

    def new_search(self):

        self.scale = 1.0
       
        self.remove_widget(self.uibc)
        self.remove_widget(self.uis)
        self.remove_widget(self.uipup)
        self.canvas.clear()
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



 


'''
                                NODE CLASSES
'''

class Node(Widget):
    asynci = ObjectProperty(None)
    def display(self, link):
        self.source = link
        return

    def on_touch_down(self, touch):
        print self.pos[0], self.pos[1]
        if (abs(touch.x - self.pos[0]) <=2*(self.width) and abs(touch.y - self.pos[1]) <= 2*(self.height)):
            print "here"
        return

     
'''
                            END NODE CLASSES
'''   


'''
                        UI INITIAL SEARCH CLASSES
'''


class UITextInput(TextInput):

    def on_touch_up(self, touch):
        if (abs(touch.x - self.center_x) <=self.width/2 and abs(touch.y - self.center_y) <= self.height/2):
            self.text = ''
            super(TextInput, self).on_touch_up(touch)
        return


'''
                        END UI INITIAL SEARCH CLASSES
'''




class WikiVizApp(App):


    def build(self):
        bkgrd = UIC()
 
       
        return bkgrd


if __name__=='__main__':
    WikiVizApp().run()
        
