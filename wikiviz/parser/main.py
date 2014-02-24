"""@package parser

Text Parser Test
"""

from root import parser
from bs4 import BeautifulSoup

""" make 'soup' from given Wikipedia page (entered manually here) """
soup = BeautifulSoup(open("rockabilly.html"), from_encoding="UTF-8")

""" print out page and image links
print "PAGE LINKS"
print "**********"
parser.get_links(soup)
print " "


print "IMAGE LINKS"
print "***********"
parser.get_pics(soup)
