import os
os.environ['GST_PLUGIN_PATH'] = r"C:\Kivy\gstreamer\lib\gstreamer-0.10"
os.environ['GST_REGISTRY'] = r"C:\Kivy\gstreamer\registry.bin"
os.environ['PATH'] = r"C:\Kivy;C:\Kivy\Python27;C:\Kivy\gstreamer\bin;C:\Kivy\MinGW\bin;%PATH%"

import kivy
kivy.require('1.8.0')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.properties import StringProperty
from controller.parser import parser

#remove once we can get the summary from the network
current_path = os.path.dirname(os.path.realpath(__file__))

url = current_path + "\knitting.html"
opened_url = open(url)

p = parser.Parser(raw_page_content=opened_url)
p.get_text_summary()
summary = p.wrapped_summary

class SummaryBox(Widget):
        summary_box = StringProperty(summary)
        
class SummaryApp(App):
    def build(self):
        return SummaryBox()

if __name__ == '__main__':
    SummaryApp().run()
