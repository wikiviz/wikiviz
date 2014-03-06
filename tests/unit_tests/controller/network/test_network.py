# -*- coding: utf-8 -*-
""" utf coding required to deal with html data """


import unittest
import wikiviz.controller.network.network as network


class NetworkTests(unittest.TestCase):
    # scaffolding data
    temp_result = "Lorem ipsum dolor sit amet"
    keyword = "Mozart"

    def test_init(self):
        # test for init
        instance = network.Network()
        self.assertTrue(instance)

        # test for singleton state
        instance_2 = network.Network()
        self.assertEqual(instance, instance_2)


    def test_on_success(self):
        """ todo: test that page data is written to Page object """
        self.assertTrue(self.temp_result)

    def test_on_error(self):
        pass

    def test_get_page(self):
        """ todo: test keywords for malformed input """
        self.assertTrue(self.keyword)


if __name__ == '__main__':
    unittest.main()