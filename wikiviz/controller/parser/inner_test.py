import unittest
from bs4 import BeautifulSoup
import wikiviz.controller.parser.parser as parser
import os
import urllib


#current_path = os.path.dirname(os.path.realpath(__file__))
#soup = BeautifulSoup(open(current_path + "/knitting.html"), from_encoding="UTF-8")


html = urllib.urlopen('http://en.wikipedia.org/wiki/Knitting').read()
h = html.decode('utf-8')
soup = BeautifulSoup(h)

p = parser.Parser()

link_list, pic_list = p.get_links(soup)
p.prioritize_links(link_list, "Knitting")