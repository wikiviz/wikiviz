
import wikiviz.controller.parser.parser as parser
import os
from bs4 import BeautifulSoup

page_data = open('page_data.txt', 'w')

#remove, once hooked up with network
current_path = os.path.dirname(os.path.realpath(__file__))

url = current_path + "\Knitting.html"
opened_url = open(url)

p = parser.Parser(raw_page_content=opened_url)

#extracts both url and image links
p.extract_links()

p.prioritize_links(p, "knitting")

p.get_text_summary()

