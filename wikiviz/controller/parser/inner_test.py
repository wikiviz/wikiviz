
import wikiviz.controller.parser.parser as parser
import os
from bs4 import BeautifulSoup

page_data = open('page_data.txt', 'w')

#remove, once hooked up with network
current_path = os.path.dirname(os.path.realpath(__file__))

url = current_path + "\knitting.html"
print url
p = parser.Parser(raw_page_content = url)

link_list = p.get_links()

image_list = p.get_images()

p_link_list = p.prioritize_links(link_list, "Knitting")


distinct_link_set = p.remove_duplicates(p_link_list)


for item in distinct_link_set:
   page_data.write(item.page_url.encode('utf8')+'\n')
