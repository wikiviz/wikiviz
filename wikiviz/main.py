"""
This is the main application file. 
Contains main Kivy application logic. 
Initial structure based off Kivy docs example.
"""

from kivy.app import App
from kivy.uix.widget import Widget

import controller.controller as controller
import time


class WikivizGame(Widget):
    """ Tests creation of modules and creates widget on screen """
    wcontroller = controller.Controller()

    # testing keywords
    temp_keywords = ["Mozart", "Gui Programming", "Virus", "Pacific Southwest Airlines"]
    for keyword in temp_keywords:
        print "fetching ", keyword
        wcontroller.create_node(keyword)

    wcontroller.model.print_graph()

    print "Window created, everything loaded ok"


class WikivizApp(App):
    def build(self):
        """ Basic Kivy strucutre """
        return WikivizGame()


if __name__ == '__main__':
    WikivizApp().run()