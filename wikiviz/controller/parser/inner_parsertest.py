import unittest
from bs4 import BeautifulSoup
import wikiviz.controller.parser.parser as parser
import os

current_path = os.path.dirname(os.path.realpath(__file__))
soup = BeautifulSoup(open(current_path+"/knitting.html"), from_encoding="UTF-8")
search_term = "knitting"

p = parser.Parser()
link_list = p.get_links(soup)

new_link_list = p.get_link_word(link_list)

p.prioritize_links(link_list, search_term)
