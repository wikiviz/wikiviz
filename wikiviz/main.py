"""
This is the main application file. 
Contains main Kivy application logic. 
Initial structure based off Kivy docs example.
"""

from kivy.app import App
from kivy.uix.widget import Widget

import display.display as display
# import controller.parser.parser as parser
import controller.network.network as network


class WikivizGame(Widget):
    """ Tests creation of modules and creates widget on screen """
    wnetwork = network.Network()
    wnetwork.get_page("Pacific_Southwest_Airlines")

    wdisplay = display.Display()
    # wparser = parser.Parser()
    print "Window created, everything loaded ok"


class WikivizApp(App):
    def build(self):
        """ Basic Kivy strucutre """
        return WikivizGame()


if __name__ == '__main__':
    WikivizApp().run()