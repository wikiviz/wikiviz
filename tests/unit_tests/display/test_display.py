'''
kivy fucking blows for unit testing.
this test is a waste of time because the damn .kv doesn't instantiate uis and uibc 
when I dynamicaly create UIC() object.
'''

import kivy
kivy.require('1.8.0')
import unittest
from wikiviz.wikiviz.display.display import *




class DisplayTests(unittest.TestCase):
    # scaffolding data
    temp_result = "Lorem ipsum dolor sit amet"
    keyword = "Mozart"

    def test_search_button(self):
        x = UIC()
        x.uis = UISearch()
        x.uibc = UIBContainer()
        x.register_event_type('on_test')
        x.bind( on_test = x.new_search)
        x.dispatch('on_test', None)
        if x.pos != (0,0):
            print 'FAILED'
        if x.scale != 1.0:
            print 'FAILED'
        if len(x.contents) != 2:
            print 'FAILED'

        


if __name__ == '__main__':
    unittest.main()