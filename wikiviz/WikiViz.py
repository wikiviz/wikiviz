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

from kivy.uix.scrollview import ScrollView
from kivy.uix.pagelayout import PageLayout
from kivy.properties import ObjectProperty, StringProperty, NumericProperty, ListProperty, BooleanProperty, DictProperty
from kivy.animation import Animation
from kivy.core import window
from kivy.utils import platform
from kivy.uix.image import AsyncImage
from kivy.uix.label import Label

from ui_classes.controls import ControlsLayout, ResetSearchPopup
from ui_classes.ui_container import UIContainer
from ui_classes.startupimage import StartupImage
from controller.controller import NetworkController
from ui_classes.node import WikiPediaUINode
from ui_classes.edge import Edge
from ui_classes.summarybox import UISummary

#
# CONTAINER LAYOUT
#
 






#
# APPLICATION ENTRY POINT
#

class WikiVizApp(App):
    ''' Main Application. Entry point for Kivy.
    '''
    def build(self):
 
        bkgrd=UIContainer(NetworkController, WikiPediaUINode, Edge)
        return bkgrd


if __name__ == '__main__':
    WikiVizApp().run()
