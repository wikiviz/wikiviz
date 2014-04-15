
import wikiviz.controller.parser.parser as parser
import os
from bs4 import BeautifulSoup

page_data = open('page_data.txt', 'w')

#remove, once hooked up with network
current_path = os.path.dirname(os.path.realpath(__file__))

url = current_path + "\cercyon.html"
opened_url = open(url)

p = parser.Parser(raw_page_content=opened_url)

p.extract_links()
p.extract_images()
p.prioritize_links(p, "cercyon")

p.get_text_summary()
#
# for item in p.link_list:
#     page_data.write(item.page_url.encode('utf8')+'\n')

