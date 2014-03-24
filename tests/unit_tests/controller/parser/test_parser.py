import unittest
from bs4 import BeautifulSoup
import wikiviz.controller.parser.parser as parser
import os

current_path = os.path.dirname(os.path.realpath(__file__))
soup1 = BeautifulSoup(open(current_path + "/knitting.html"), from_encoding="UTF-8")
soup2 = BeautifulSoup(open(current_path + "/sarah_stone.html"), from_encoding="UTF-8")

class ParserTests(unittest.TestCase):

    def test_init(self):
        p = parser.Parser()
        # test that p is not empty
        self.assertTrue(p)


    def test_get_links(self):
        """test page with internal Wiki links"""
        p = parser.Parser()
        p.get_links(soup1)
        self.assertTrue(p)

        """test dead-end page, with no internal Wiki links"""
        p.get_links(soup2)
        self.assertTrue(p)

    def test_prioritize_links(self):

        """test link titles with high priorities and low priorities"""
        p = parser.Parser(page_name = "Knitting clubs")
        p1 = parser.Parser(page_name = "Shoemaking")
        link_list = list([p,p1])
        p.prioritize_links(link_list, "Knitting")
        self.assertTrue(p)

    def test_remove_duplicates(self):

        # is self.assertTrue(p) helpful here? does it prove anything?

        p = parser.Parser(page_url = "/wiki/Knitting_clubs", page_name = "Knitting clubs")
        p1 = parser.Parser(page_url = "/wiki/Knitting_clubs", page_name = "Knitting clubs")
        p2 = parser.Parser(page_url = "/wiki/Shoemaking", page_name = "Shoemaking")
        link_list = list([p, p1, p2])
        p.remove_duplicates(link_list)
        self.assertTrue(p)

if __name__ == '__main__':
    unittest.main()

