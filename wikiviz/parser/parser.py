"""@package parser
Main Parser Module. 

Translates keywords into related links, images, and text.
"""

from bs4 import BeautifulSoup
from types import *


class Parser():
    """ @class parser
        Main parser class description """

    def __init__(self):
        """ The constructor 
        @param self default parameter for constructor """

        print "BeautifulSoup imported"
        print "Parser created"
        
       
    def get_links(soup):
        """ Get URLS from given Wiki page 
            TODO: Omit links from outside frames """
        link_list = list()
        
        """ Omit relative links and those with no type """
        for anchor in soup.find_all('a'):
            temp_link = anchor.get('href')
            if (type(temp_link) is NoneType) or (temp_link[0] == '#'):
                continue
            else:
                link_list.append(temp_link)
                
        """Print list """
        for thing in link_list:
            print thing 
            
    def get_pics(soup):
        """ Get image links from given Wiki page """
        pic_list = list()
        
        """ Omit Wiki specific image links e.g. 'Enlarge' """
        for image in soup.find_all('img'):
            temp_img = image.get('src')
            if 'bits.wikimedia.org' in temp_img:
                continue
            else:
                pic_list.append(temp_img)
             
        """Print image links"""     
        for item in pic_list:
            print item

