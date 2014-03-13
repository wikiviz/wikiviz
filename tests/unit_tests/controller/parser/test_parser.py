import unittest
from bs4 import BeautifulSoup
import wikiviz.controller.parser.parser as parser
import os

current_path = os.path.dirname(os.path.realpath(__file__))
soup = BeautifulSoup(open(current_path + "/knitting.html"), from_encoding="UTF-8")


class ParserTests(unittest.TestCase):
    def test_init(self):
        # parser's constructor does not currently accept a parameter
        p = parser.Parser()

        # test that p is not empty
        self.assertTrue(p)

    def test_get_links(self):
        p = parser.Parser()
        p.get_links(soup)
        self.assertTrue(p)

    def test_get_link_word(self):
        p = parser.Parser("/wiki/Shoemaking")
        link_list = list()
        link_list.append(p)
        p.get_link_word(link_list)
        self.assertTrue(p)


    def test_prioritize_links(self):
        p = parser.Parser(page_name = "Knitting clubs")
        p1 = parser.Parser(page_name = "Shoemaking")
        link_list = list([p,p1])
        p.prioritize_links(link_list, "Knitting")
        self.assertTrue(p)


if __name__ == '__main__':
    unittest.main()
