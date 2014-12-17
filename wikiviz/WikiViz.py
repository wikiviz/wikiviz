"""
Application entry point.
Loads KV file and calls controller on user events.
"""

# environment variables needed by our team members
import sys
import os
if sys.platform != "darwin":
    os.environ['GST_PLUGIN_PATH'] = r"C:\Kivy\gstreamer\lib\gstreamer-0.10"
    os.environ['GST_REGISTRY'] = r"C:\Kivy\gstreamer\registry.bin"
    os.environ['PATH'] = r"C:\Kivy\gstreamer\bin;%PATH%"


from kivy import require
require('1.8.0')
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup

from kivy.uix.pagelayout import PageLayout
from kivy.properties import ObjectProperty, StringProperty, NumericProperty, ListProperty, BooleanProperty, DictProperty
from kivy.animation import Animation
from kivy.core import window
from kivy.utils import platform



from ui_classes.ui_container import UIContainer 
from ui_classes.startupimage import StartupImage
from controller.controller import NetworkController
from ui_classes.node import WikiPediaUINode
from ui_classes.edge import Edge
#
# CONTAINER LAYOUT
#

class Scatter_Summary_Widget(PageLayout):
    ''' Container layout for application.
    Contains UIContainer, Summary, and uibc (?)
    '''
    uic = ObjectProperty(None)
    summary = ObjectProperty(None)
    controls = ObjectProperty(None)


    def __init__(self, **kwargs):
        super(Scatter_Summary_Widget, self).__init__(**kwargs)
        
        #children are created in reverse order
        #reverse order of children in self.children to align with self.page
        self.summary = UISummary()
        self.uic = UIC(self.add_controls)
        self.add_widget(self.summary)
        self.add_widget(self.uic)
        self.page_dict = {"summary":0, "ui_container":1, 'controls':2}

    def add_controls(self):
        self.controls = ControlsLayout()
        self.add_widget(self.controls)
        self.show_ui_container()
    def show_summary(self):
        self.page = 0
        self.do_layout()
    def show_ui_container(self):
        self.page =1 
        self.do_layout()

    def do_layout(self, *largs):
        ''' Override do_layout.
            Slide screen in from left with animation.
        '''
        for i, c in enumerate(self.children):

            width = self.width 


            if i < self.page:
                x = self.right
            elif i == self.page:
                x = self.x
            elif i > self.page:
                x = self.right

            c.width = width
            c.height = self.height       

            if i == self.page:
                Animation(
                    x=x,
                    y=self.y,
                    d=0.5, t='in_quad').start(c)


    def on_touch_down(self, touch):
        return (self.children)[self.page].on_touch_down(touch)


    def on_touch_move(self, touch):
        return (self.children)[self.page].on_touch_move(touch)


    def on_touch_up(self, touch):
        return (self.children)[self.page].on_touch_up(touch)



#
# APPLICATION ENTRY POINT
#

class WikiVizApp(App):
    ''' Main Application. Entry point for Kivy.
    '''


    def build(self):

        bkgrd = UIContainer(NetworkController, WikiPediaUINode, Edge)

        return bkgrd


if __name__ == '__main__':
    WikiVizApp().run()
