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
from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout
from controller.parser import parser

#remove once we can get the summary from the network
current_path = os.path.dirname(os.path.realpath(__file__))

url = current_path + "\Knitting.html"
opened_url = open(url)

#get images
p = parser.Parser(raw_page_content=opened_url)
img_srcs = p.get_images(5)
main_image = img_srcs[0]

#get text summary
#currently doesn't maintain all the '\n', not sure why atm
summary = p.get_text_summary()

class SummaryBox(GridLayout):
        summary_box = StringProperty(summary)
        image = ObjectProperty(main_image)

class SummaryApp(App):
    def build(self):
        return SummaryBox()

if __name__ == '__main__':
    SummaryApp().run()
