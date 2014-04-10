import os
os.environ['GST_PLUGIN_PATH'] = r"C:\Kivy\gstreamer\lib\gstreamer-0.10"
os.environ['GST_REGISTRY'] = r"C:\Kivy\gstreamer\registry.bin"
os.environ['PATH'] = r"C:\Kivy;C:\Kivy\Python;C:\Kivy\gstreamer\bin;C:\Kivy\MinGW\bin;%PATH%"

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
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.properties import ObjectProperty, StringProperty, NumericProperty, ListProperty, BooleanProperty
from kivy.graphics import Line, Color
from kivy.graphics.transformation import Matrix
from kivy.graphics.stencil_instructions import StencilPush, StencilPop, StencilUse
from kivy.animation import Animation
from kivy.core import window


from controller.controller import Controller



import sys
from kivy.utils import boundary, platform


_platform = platform

# for reloading, we need to keep a list of textinput to retrigger the rendering

# cache the result
_is_osx = sys.platform == 'darwin'

# When we are generating documentation, Config doesn't exist
_is_desktop = False



'''
To Do

1. slider
2. Work on Model

Model needs a data structure to hold the nodes.
?Possibly use binary tree.
?Restructure tree using traversal and number of nodes in tree.

?Possibly position buckets using a dict

?Possibly double linked list and bubble sort.

1.Use data structure to test for collisions
Use data structure to retrieve teh text and images.

2.Use model information to add nodes and edges.


TIPS:
If you cannot load the images change kivy.loader.py LoaderBase class
change the line suffix = mimetype.guess_extension to None.

'''






text1='''

[b]Mozart\n[/b]
Musican\n
01234567890123456789012345678901234567890123456789\n
[color=#3333ff]died:\n[/color]
Location\n
Works:\n
Acomplishments:\n
Contributions:\n
Mozart\n
Musican\n
born:\n
died:\n
Location\n
Works:\n
Acomplishments:\n
Contributions:\n
Mozart\n
Musican\n
born:\n
died:\n
Location\n
Works:\n
Acomplishments:\n
Contributions:\n
Mozart\n
Musican\n
born:\n
died:\n
Location\n
Works:\n
Acomplishments:\n
Contributions:\n
Musican\n
born:\n
died:\n
Location\n
Works:\n
Acomplishments:\n
Contributions:\n
Works:\n
Acomplishments:\n
Contributions:\n
Musican\n
born:\n
died:\n
Location\n
Works:\n
Acomplishments:\n
Contributions:\n


'''
class ProxyModelNode(object):
    def __init__(self):
        self.text = text1
        self.source = ""



'''
                                NODE CLASSES
'''
class Node(Scatter):
    image = ObjectProperty(None)
    label = ObjectProperty(None)

    model_node = ObjectProperty(None)

    move = NumericProperty(0)
    flag = NumericProperty(0)

    def __init_(self, **kwargs):
        
        super(Node, self).__init__(kwargs)
        self.do_rotation = False
        self.do_scale = False
        self.do_translation = False
        self.flag = 0
        

    def collide_point(self, x, y):
        x, y = self.to_local(x, y)
        return -1.1*self.width/8 <= x <= 1.2*self.width and -1.1*self.height/8 <= y <= 1.2*self.height

    def on_touch_up(self, touch):   
        if (self.collide_point(touch.x, touch.y) and self.move < 10):
            pagelayout = self.parent.parent
            uic = pagelayout.uic
            pagelayout.page = 2

            Controller().create_node(self, self.label.text)

            pagelayout.do_layout()
            pagelayout.summary.text = text1
            uic.blocked = True
            Animation(
                x=(-self.x)*uic.scale+window.Window.width/2,
                y=(-self.y)*uic.scale+window.Window.height/2,
                d=.5, t='in_quad').start(self.parent.parent.uic)
        if touch in self._touches:
            touch.ungrab(self)
            del self._last_touch_pos[touch]
            self._touches.remove(touch)
        return super(Node, self).on_touch_up(touch)


    def on_touch_move(self, touch):
        self.move +=1
        return super(Node, self).on_touch_move(touch)


    def on_touch_down(self, touch):
        self.move = 0
        return super(Node, self).on_touch_down(touch)

    def on_node_creation(self):
        self.model_node = ProxyModelNode()

    def display(self, link):
        self.image.source = link
        return
    def create_children(self, model_node):
        print "creating child"
        pagelayout = self.parent.parent
        uic = pagelayout.uic
        uic.dispatch("on_add_node", model_node)


'''
                            END NODE CLASSES
''' 




class Edge(Widget):
    p = ObjectProperty(None)
    c = ObjectProperty(None)  

    def __init__(self,parent, child, **kwargs):
        self.p = parent
        self.c = child

        super(Edge, self).__init__(**kwargs)

    def collide_point(self, x, y):
        return False

    def on_touch_down(self, touch):
        return
    def on_touch_up(self, touch):
        return
    def on_touch_move(self, touch):
        return


class StartupImage(Image):
    def collide_point(self, x, y):
        return False
    def on_touch_down(self, touch):
        return
    def on_touch_up(self, touch):
        return
    def on_touch_move(self, touch):
        return




class UIC(ScatterPlane):

    is_popup_displayed = BooleanProperty(False)

    blocked = BooleanProperty(False)

    controller = ObjectProperty(None)

    def __init__(self, **kwargs):



        super(UIC, self).__init__(**kwargs)
        

        self.do_rotation = False
        self.do_scale = False
        self.do_translation= False

        self.register_event_type("on_add_node")


       

        return




########################## OVERRIDE FUNCTIONS##############################################
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
                #super(Scatter, self).on_touch_down(touch)
                eachChild.on_touch_down(touch)
                touch.pop()
                self._bring_to_front()
                return False

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
            for eachChild in self.children:
                if eachChild.collide_point(touch.x, touch.y):
                    #super(Scatter, self).on_touch_up(touch)
                    eachChild.on_touch_move(touch)
                    touch.pop()
                    self._bring_to_front()
                    return False
            touch.pop()
        if touch in self._touches and touch.grab_current == self:
            if self.transform_with_touch(touch):
                self.dispatch('on_transform_with_touch', touch)
            self._last_touch_pos[touch] = touch.pos
        if self.collide_point(x, y):
            return True

    def on_touch_up(self, touch):
        print " touch up uic"
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
            for eachChild in self.children:
                if eachChild.collide_point(touch.x, touch.y):
                    #super(Scatter, self).on_touch_up(touch)
                    eachChild.on_touch_up(touch)
                    self._bring_to_front()
                    #touch.pop()
                    self._bring_to_front()
                    break

            touch.pop()
        if touch in self._touches:
            touch.ungrab(self)
            del self._last_touch_pos[touch]
            self._touches.remove(touch)
        if self.collide_point(x, y):
            return True
############################################################################################

    def display(self):   
        self.uis.disabled= True
        keyword= self.uis.search_bar.text 
        self.remove_widget(self.uis)

        
 
        

        self.do_scale = True
        self.do_translation= True
   
        
        
        #The code below is just to demonstrate how to
        #use the network to request new nodes from within the display.
        
        # get instance of Network object
        print "Initing network object"
        self.controller = Controller()

     

        # run a few queries for demo purposes
        print "Querying for" + self.uis.search_bar.text
        self.controller.create_node(self, self.uis.search_bar.text)



        '''
                    This code will be deleted when model is hoooked up
        '''
        node = Node(size=(100,100), pos=(200,450))
        self.add_widget(node)
        node.display("http://i1164.photobucket.com/albums/q572/marshill2/sun_zps0fa10dc5.jpg")
        for i in range(1,10):
            x = Node(size=(100,100), pos=(0,i*100))  
            x.display("http://i1164.photobucket.com/albums/q572/marshill2/sun_zps0fa10dc5.jpg")
            x.label.text = self.uis.search_bar.text
            self.add_widget(x)
            self.add_widget(Edge(node,x))
            node._bring_to_front()
            x._bring_to_front()
        


        '''
                            END DELETEION
        '''
        return
    def on_add_node(self, model_node):
        return

    def create_child(self, model_node):
        x = Node(pos = model_node.get_pos())
        x.display(model_node.get_source())
        x.label.text = model_node.get_keyword()
        self.add_widget(x)









class Scatter_Summary_Widget(PageLayout):
    uic = ObjectProperty(None)
    summary = ObjectProperty(None)
    uibc = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(Scatter_Summary_Widget, self).__init__(**kwargs)

        self.uic.remove_widget(self.uic.uipup)
        self.uibc.disabled = True
        self.uibc.opacity = 0

########################## OVERRIDE FUNCTIONS##############################################
    def do_layout(self, *largs):
        l_children = len(self.children)
        for i, c in enumerate(reversed(self.children)):
            if isinstance(c, BoxLayout):
                continue
            if i < l_children:
                height = self.height - self.border
            else:
                height = self.height - 2 * self.border

            if i == 0:
                self.uic.blocked = False
                y = self.y

            elif i < self.page:
                y = self.y

            elif i == self.page:
                y = self.y + self.border

            elif i == self.page + 1:
                y = self.top - self.border

            else:
                y = self.top


            c.height = height
            c.width = self.width       
            if i != 0:
                Animation(
                    x=self.x,
                    y=y,
                    d=0.5, t='in_quad').start(c)

    def on_touch_down(self, touch):
        print self.children
        if (self.children[1].collide_point(touch.x, touch.y)):
            return self.children[1].on_touch_down(touch)
        return self.children[len(self.children) - self.page-1].on_touch_down(touch)

    def on_touch_move(self, touch):
        if (self.children[1].collide_point(touch.x, touch.y)):
            return self.children[1].on_touch_move(touch)
        return self.children[len(self.children) -self.page-1].on_touch_move(touch)

    def on_touch_up(self, touch):
        print "ROOT TOUCH UP"
        if (self.children[1].collide_point(touch.x, touch.y)):
            return self.children[1].on_touch_up(touch)
        return self.children[len(self.children) -self.page-1].on_touch_up(touch)
############################################################################################
    
class UISummary(ScrollView):
    flag = BooleanProperty(False)
    text = StringProperty(None)
########################### OVERRIDE FUNCTIONS #############################################
    def on_touch_up(self, touch):
        if self.flag:
            self.flag = False
            self.parent.page = 0
            self.parent.do_layout()
        return super(UISummary, self).on_touch_up(touch) 
    def on_touch_move(self, touch):
        if self._get_uid('svavoid') in touch.ud:
            return
        if self._touch is not touch:
            # touch is in parent
            touch.push()
            touch.apply_transform_2d(self.to_local)
            super(ScrollView, self).on_touch_move(touch)
            touch.pop()
            return self._get_uid() in touch.ud
        if touch.grab_current is not self:
            return True

        uid = self._get_uid()
        ud = touch.ud[uid]
        mode = ud['mode']

        # check if the minimum distance has been travelled
        if mode == 'unknown' or mode == 'scroll':
            if self.do_scroll_x and self.effect_x:
                width = self.width
                if self.scroll_type != ['bars']:
                    self.effect_x.update(touch.x)
            if self.do_scroll_y and self.effect_y:
                height = self.height
                if self.scroll_type != ['bars']:
                    self.effect_y.update(touch.y)

        if (touch.dy !=0 and abs(touch.dx/touch.dy) >1) or (touch.dy==0 and abs(touch.dx) > 3):
            self.flag = True
            return True

        if mode == 'unknown':
            ud['dx'] += abs(touch.dx)
            ud['dy'] += abs(touch.dy)
            if ud['dx'] > self.scroll_distance:
                if not self.do_scroll_x:
                    # touch is in parent, but _change expects window coords
                    touch.push()
                    touch.apply_transform_2d(self.to_local)
                    touch.apply_transform_2d(self.to_window)
                    self._change_touch_mode()
                    touch.pop()
                    return
                mode = 'scroll'

            if ud['dy'] > self.scroll_distance:
                if not self.do_scroll_y:
                    # touch is in parent, but _change expects window coords
                    touch.push()
                    touch.apply_transform_2d(self.to_local)
                    touch.apply_transform_2d(self.to_window)
                    self._change_touch_mode()
                    touch.pop()
                    return
                mode = 'scroll'
            ud['mode'] = mode

        if mode == 'scroll':
            ud['dt'] = touch.time_update - ud['time']
            ud['time'] = touch.time_update
            ud['user_stopped'] = True

        return True
############################################################################################

class MyTextInput(TextInput):
    def __init__(self, **kwargs):
        super(MyTextInput, self).__init__(**kwargs)
        self.register_event_type("on_enter")
########################### OVERRIDE FUNCTIONS #############################################
    def _keyboard_on_key_down(self, window, keycode, text, modifiers):
        # Keycodes on OSX:
        ctrl, cmd = 64, 1024
        key, key_str = keycode

        # This allows *either* ctrl *or* cmd, but not both.
        is_shortcut = (modifiers == ['ctrl'] or (
            _is_osx and modifiers == ['meta']))
        is_interesting_key = key in (list(self.interesting_keys.keys()) + [27])

        if not self._editable:
            # duplicated but faster testing for non-editable keys
            if text and not is_interesting_key:
                if is_shortcut and key == ord('c'):
                    self._copy(self.selection_text)
            elif key == 27:
                self.focus = False
            return True

        if text and not is_interesting_key:
            self._hide_handles(self._win)
            self._hide_cut_copy_paste()
            self._win.remove_widget(self._handle_middle)
            if is_shortcut:
                if key == ord('x'):  # cut selection
                    self._cut(self.selection_text)
                elif key == ord('c'):  # copy selection
                    self._copy(self.selection_text)
                elif key == ord('v'):  # paste selection
                    self._paste()
                elif key == ord('a'):  # select all
                    self.select_all()
                elif key == ord('z'):  # undo
                    self.do_undo()
                elif key == ord('r'):  # redo
                    self.do_redo()
            else:
                if self._selection:
                    self.delete_selection()
                self.insert_text(text)
            #self._recalc_size()
            return


        if key == 27:  # escape
            self.focus = False
            return True
        elif key == 9:  # tab
            self.insert_text(u'\t')
            return True
        elif key == 13: # enter
            self.dispatch("on_enter")
            return True

        k = self.interesting_keys.get(key)
        if k:
            key = (None, None, k, 1)
            self._key_down(key)
############################################################################################
    def on_enter(self):
        return

class WikiVizApp(App):

    bkgrd = ObjectProperty(None)


    def build(self):

        bkgrd= Scatter_Summary_Widget()
        return bkgrd

if __name__=='__main__':
    WikiVizApp().run()
        
