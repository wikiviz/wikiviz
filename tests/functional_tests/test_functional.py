# functionaltest.py


""" functional end-to-end tests """

import unittest
import wikiviz.controller.network.network as network
import wikiviz.display.display as display


class FunctionalTests(unittest.TestCase):
    
    def test_app(self):
        wnetwork = network.Network()
        wnetwork.get_page("Pacific_Southwest_Airlines")
        self.assertTrue(wnetwork)



if __name__ == '__main__': 
    unittest.main() 