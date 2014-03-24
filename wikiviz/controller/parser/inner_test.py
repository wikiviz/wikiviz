import unittest
from bs4 import BeautifulSoup
import wikiviz.controller.parser.parser as parser
import os
import urllib

f = open('workfile.txt', 'w')


current_path = os.path.dirname(os.path.realpath(__file__))
soup = BeautifulSoup(open(current_path + "/knitting.html"), from_encoding="UTF-8")

p = parser.Parser()

link_list, pic_list = p.get_links(soup)
p_link_list = p.prioritize_links(link_list, "Knitting")
distinct_link_set = p.remove_duplicates(p_link_list)
for item in distinct_link_set:
    f.write(item.page_url.encode('utf8')+'\n')