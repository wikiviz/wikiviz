"""@package parser
Main Parser Module. 

Translates keywords into related links, images, and text.
"""

from bs4 import BeautifulSoup
from types import NoneType


class Parser():
    """ @class parser
        Main parser class description """

    def __init__(self):
        """ The constructor 
        @param self default parameter for constructor """

        print "BeautifulSoup imported"
        print "Parser created"
        
       
    """
    get links
    """
    def get_links(soup):
    
        link_list = list()
    
        """ use keywords list to filter out undesirable elements"""
        filtered_keywords = ('Help:', 'Category:', 'Talk:', 'Special:', 'Wikipedia:', 'File:')
    
        """ get links from wiki article that have a type and are NOT anchors """
        for anchor in soup.find_all('a'):
            temp_link = anchor.get('href')
            if type(temp_link) is not NoneType and temp_link.startswith('/wiki/'):
                link_list.append(temp_link)
    
            for keyword in filtered_keywords:
                for item in link_list:
                    if keyword in item:
                        link_list.remove(item)
       
        """create distinct set of links"""
        distinct_link_list = list(set(link_list))
        
        """ print list """
        for elem in distinct_link_list:
            print elem 
     
    """
    get images: 
    ignore //bits.wikimedia.org
    only use //upload.wikimedia.org

    """

    def get_pics(soup):
        pic_list = list()
    
        """ add only images themselves to list """
        for image in soup.find_all('img'):
            temp_img = image.get('src')
            if 'bits.wikimedia.org' in temp_img:
                continue
            else:
                pic_list.append(temp_img)
         
        """ print image links """     
        for item in pic_list:
            print item

    """
    end function defs
    """


    """ Create BeautifulSoup object from given HTML page and specify unicode version """
    
    """ TODO: try out with many different Wikipedia pages; currently have Knitting and Rockabilly """

    soup = BeautifulSoup(open("rockabilly.html"), from_encoding="UTF-8")

    get_links(soup)

    #get_pics(soup)


