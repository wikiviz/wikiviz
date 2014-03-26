
import wikiviz.controller.parser.parser as parser
import os
from bs4 import BeautifulSoup

page_data = open('page_data.txt', 'w')

#remove, once hooked up with network
current_path = os.path.dirname(os.path.realpath(__file__))
soup = BeautifulSoup(open(current_path + "\knitting.html"), from_encoding="UTF-8")

p = parser.Parser()

link_list = p.get_links(soup)

image_list = p.get_images(soup)

p_link_list = p.prioritize_links(link_list, "Knitting")


#distinct_link_set = p.remove_duplicates(p_link_list)


#for item in distinct_link_set:
 #   page_data.write(item.page_url.encode('utf8')+'\n')
#
# page_data.write("***************************" + '\n')
#
# for pic in pic_list:
#     page_data.write(pic.page)