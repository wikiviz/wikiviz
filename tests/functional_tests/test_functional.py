"""
    integration and end-to-end tests
    run with 'nosetests -s test_functional.py'
    the -s flag allows print statements to work
"""

import unittest
import wikiviz.controller.network.network as network


class FunctionalTests(unittest.TestCase):
    def setUp(self):
        "set up test fixtures; run automatically"
        self.wnetwork = network.NetworkRequest(None, self.testNetworkSuccess)

    def testNetwork(self):
        print "testing network init"
        self.assertTrue(self.wnetwork)

    def testNetworkGetPage(self):
        print "testing network get page"
        self.wnetwork.get_page("Pacific_Southwest_Airlines")

    def testNetworkSuccess(self):
        print "network response returned"
        # self.assertTrue(completed_request)
        # self.assertTrue(model_node)



if __name__ == '__main__': 
    unittest.main() 