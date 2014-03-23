import kivy
kivy.require('1.8.0')

from random import random 
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
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.graphics import Line, Color
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

    def display(self, link):
        self.image.source = link
        return
    def on_touch_up(self, touch):
        print "TOUCH NODE UP", touch.x, touch.y
        if (abs(touch.x - self.pos[0]) <=(self.width) and abs(touch.y - self.pos[1]) <= (self.height)):
            if ( self.move < 5 and self.flag ==0):
                self.parent.parent.page+= 1
                self.parent.parent.summary.text = "INSERT SUMMARY HERE"
                self.parent.parent.uic.disabled = True
                self.flag = 1

        return super(Node, self).on_touch_up(touch)

        return
    def on_touch_move(self, touch):
        self.move+=1
        return super(Node, self).on_touch_move(touch)


    def on_touch_down(self, touch):
        self.move =0 
        self.flag = 0
        return super(Node, self).on_touch_down(touch)
        

     
'''
                            END NODE CLASSES
'''   






class UIC(ScatterPlane):
    flag2 = NumericProperty(0)

    def __init__(self, **kwargs):

        super(UIC, self).__init__(**kwargs)
        
        
        #self.uibc.disabled = True


        self.do_rotation = False
        self.do_scale = False
        self.do_translation= False


        #self.remove_widget(self.uibc)
        #self.remove_widget(self.uipup)

        #self.controller = Controller()

       

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

    def connect_with_line(self,coord1, coord2):
        print random()
        with self.canvas:
            Color(random(),random(),random())
            Line(points = [coord1[0], coord1[1], coord2[0], coord2[1]], width=2)

    def confirm_new_search(self):
        print "CONFIRM"
        print "FLAG", self.flag2
        if self.flag2 == 0:
            self.add_widget(self.uipup)
            self.flag2 = 1

    def new_search(self):

        self.scale = 1.0
       
        self.remove_widget(self.uibc)
        self.remove_widget(self.uis)
        self.remove_widget(self.uipup)
        self.flag2 = 0
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

    def on_touch_move(self, touch):
        for eachChild in self.children:
            if eachChild.on_touch_move(touch):
                print "IN CHILD"
                return
        super(UIC, self).on_touch_move(touch)
        return
    def on_touch_up(self, touch):
        for eachChild in self.children:
            if eachChild.on_touch_up(touch):
                print "IN CHILD"
                return
        super(UIC, self).on_touch_up(touch)
        return
    def on_touch_down(self, touch):
        for eachChild in self.children:
            if eachChild.on_touch_down(touch):
                print "IN CHILD"
                return
        super(UIC, self).on_touch_down(touch)
        return
    def in_child(self, child, touch):
        if ((child.center_x - touch.x < child.width/2) and (child.center_y - touch.y < child.height/2)):
            return True
        return False
 
    def remove_widget(self, to_remove):
        super(UIC, self).remove_widget(to_remove)
        self.flag2 = 0
        return 0

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

class UIPopup(Popup):
    def on_touch_down(self,touch):
        if (abs(touch.x - self.center_x) <=self.width/2 and abs(touch.y - self.center_y) <= self.height/2):
            super(UIPopup, self).on_touch_down(touch)
            return True
        return False
    def on_touch_up(self,touch):
        if (abs(touch.x - self.center_x) <=self.width/2 and abs(touch.y - self.center_y) <= self.height/2):
            super(UIPopup, self).on_touch_up(touch)
            return True
        return False
    def on_touch_move(self,touch):
        if (abs(touch.x - self.center_x) <=self.width/2 and abs(touch.y - self.center_y) <= self.height/2):
            super(UIPopup, self).on_touch_move(touch)
            return True
        return False
        

            


class test(PageLayout):
    uic = ObjectProperty(None)
    summary = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(test, self).__init__(**kwargs)
        self.uic.remove_widget(self.uic.uipup)
        self.uic.remove_widget(self.uic.uibc)

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

    def do_nothing(self, *args):
        return
    def on_touch_down(self, touch):
        print self.page
        return self.children[self.page - 1].on_touch_down(touch)

    def on_touch_move(self, touch):
        print self.page
        return self.children[self.page - 1].on_touch_move(touch)

    def on_touch_up(self, touch):
        print self.page
        return self.children[self.page-1].on_touch_up(touch)
    
class UISummary(ScrollView):

    text = StringProperty(None)

    def on_touch_down(self, touch):
        print "here down"
        return 

    def on_touch_up(self, touch):
        print "here up"
        self.parent.uic.disabled = False
        self.parent.page -= 1
        return
        

class gr(ScatterPlane):
    container = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(gr, self).__init__(**kwargs)
        self.do_rotation = False

    def on_touch_move(self, touch):
        print "MOVE"
        for eachChild in self.children:
            if eachChild.on_touch_move(touch):
                return
        super(gr, self).on_touch_move(touch)
        return

    def on_touch_up(self, touch):
        print "UP"
        for eachChild in self.children:
            if eachChild.on_touch_up(touch):
                return
        super(gr, self).on_touch_up(touch)
        return

    def on_touch_down(self, touch):
        print "DOWN"
        for eachChild in self.children:
            if eachChild.on_touch_down(touch):
                return
        super(gr, self).on_touch_down(touch)
        return

class sc(Scatter):
    image = ObjectProperty(None)

    def on_touch_move(self, touch):
        print "MOVE"
        return super(sc, self).on_touch_move(touch)

    def on_touch_up(self, touch):
        print "UP"
        return super(sc, self).on_touch_up(touch)

    def on_touch_down(self, touch):
        print "DOWN"
        return super(sc, self).on_touch_down(touch)

class WikiVizApp(App):

    bkgrd = ObjectProperty(None)


    def build(self):
        bkgrd= test()
#        bkgrd = gr()
#        for i in range(0, 10):
#            x = sc(pos = (i*100,i*100))
#            x.image.source = "http://i1164.photobucket.com/albums/q572/marshill2/sun_zps0fa10dc5.jpg"
#            bkgrd.add_widget(x)
#            x.pos = (i*100,i*100)

        #bkgrd.uic.add_widget(x)
        return bkgrd

if __name__=='__main__':
    WikiVizApp().run()
        
