import unittest
from bs4 import BeautifulSoup
import wikiviz.controller.parser.parser as parser
import os

current_path = os.path.dirname(os.path.realpath(__file__))
soup = BeautifulSoup(open(current_path+"/knitting.html"), from_encoding="UTF-8")

class ParserTests(unittest.TestCase):
	
	def test_init(self):
		# you need the full path for the file to open:
		

		# parser's constructor does not currently accept a parameter
		p = parser.Parser()

		# test that p is not empty
		self.assertTrue(p)

        def test_get_links(self):
            p = parser.Parser()
            p.get_links(soup)
            self.assertTrue(p)
            

	
if __name__ == '__main__':
	unittest.main()
