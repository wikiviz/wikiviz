
import unittest
from bs4 import BeautifulSoup
import parser

#######'module' object has no attribute 'Parser'######
class ParserTests(unittest.TestCase):

    """test data"""
    soup = BeautifulSoup(open("knitting.html"), from_encoding="UTF-8")


##    """ test initialization """
##    def test_init(self):
##        instance = parser.Parser()
##        self.assertTrue(instance)
##
##    def test_get_links(self, soup):
##        self.assertTrue(soup)
##        page_link_list = parser.Parser().get_links(self, soup)
##        self.assertTrue(page_link_list)
##
##    def test_get_link_word(self, link_list):
##        self.assertTrue(link_list)
##        
##        
##
##    def test_get_pics(self, soup):
##        self.assertTrue(soup)
##        image_link_list = parser.Parser().get_pics(self, soup)
##        self.assertTrue(image_link_list)


if __name__ == '__main__':
    unittest.main()        

   
