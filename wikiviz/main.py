"""
This is the main application file. 
Contains main Kivy application logic. 
Initial structure based off Kivy docs example.
"""
import kivy
kivy.require('1.8.0')
from wikiviz.wikiviz.display.display import DisplayApp

DisplayApp().run()