import unittest
from bs4 import BeautifulSoup
import wikiviz.controller.parser.parser as parser
import os

class ParserTests(unittest.TestCase):
	
	def test_init(self):
		# you need the full path for the file to open:
		current_path = os.path.dirname(os.path.realpath(__file__))
		soup = BeautifulSoup(open(current_path+"/knitting.html"), from_encoding="UTF-8")
		 
		  
		"""print out page and image links """
		print "PAGE LINKS"
		print "**********"

		# parser's constructor does not currently accept a parameter
		p = parser.Parser()

		# test that p is not empty
		self.assertTrue(p)

	
if __name__ == '__main__':
	unittest.main()