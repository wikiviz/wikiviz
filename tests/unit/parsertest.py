
from bs4 import BeautifulSoup
from parser import parser

soup = BeautifulSoup(open("knitting.html"), from_encoding="UTF-8")
 
  
"""print out page and image links """
print "PAGE LINKS"
print "**********"

parser(soup)
