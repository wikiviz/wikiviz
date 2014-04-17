"""
    integration and end-to-end tests
    run with 'nosetests test_functional.py'
"""

import unittest
import wikiviz.controller.network.network as network


class FunctionalTests(unittest.TestCase):
    def setUp(self):
        "set up test fixtures; run automatically"
        self.wnetwork = network.NetworkRequest(None, None)

    def testNetwork(self):
        self.assertTrue(self.wnetwork)

    def testNetworkGetPage(self):
        self.wnetwork.get_page("Pacific_Southwest_Airlines")

if __name__ == '__main__': 
    unittest.main() 