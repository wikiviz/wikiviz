"""@package parser
Main Parser Module. 

Translates keywords into related links, images, and text.
"""

from bs4 import BeautifulSoup
from types import NoneType

filtered_keywords = ('Help:', 'Category:', 'Talk:', 'Special:', 'Wikipedia:', 'bits.wikimedia.org', 'File:', 'en/thumb/', '.svg.', 'Portal:', 'Template:', '/Main_Page')

class Parser(object):

    
    """ @class parser
        Main parser class description """
    class PageLink():

        def __init__(self, page_url, page_priority = None):

            self.page_url = page_url
            self.page_priority = page_priority

##        def get_attributes(self):
##
##            return get_page_url
##
##        def get_page_priority(self):
##
##            return page_priority


    class ImageLink():

        def __init__(self, page_url, page_priority = None):

            self.page_url = page_url
            self.page_priority = page_priority

##        def get_attributes(self):
##
##            return get_page_url
##
##        def get_page_priority(self):
##
##            return page_priority
        
    def __init__(self, page_url = None, page_priority = None):

        self.page_url = page_url
        self.page_priority = page_priority
        
    
    """ 
    function definitions
    
    """
    
    """
    get links
    page and image links are currently separate
    """
    
    def get_links(self, soup):
        
        link_list = list()
        
               
        """ get links from wiki article that have a type and are NOT anchors """
        for anchor in soup.find_all('a'):
            page_url = anchor.get('href')
            
            """ initially set priority to 3, just for starters"""
            
            if type(temp_link.page_url) is not NoneType and temp_link.page_url.startswith('/wiki/'):
                link_list.append(temp_link)
        """ use keywords list to filter out undesirable elements"""
        for keyword in filtered_keywords:
                for item in link_list:
                    if keyword in item.page_url:
                        link_list.remove(item)
                        
        
        """create distinct set of links"""
        """ do this after prioritizing! """
        #distinct_link_list = list(set(link_list))
        
        """ print list """
        for elem in link_list:
            print elem.page_url
            

        
            
##    """
##    get word alone
##    
##    """
##    def get_link_word(self, link_list):
##    
##        link_word_list = list()
##        
##        for word in link_list:
##            link_word = PageLink(word.page_url, 3)
##            
##            link_word_list.append(word.page_url[6:])
##            
##            
##        ##hmm but you want the url too, right?
##            
##        for link_word in link_word_list:
##            if "_" in link_word:
##                print link_word
##             
##            
    """
    get images: 
    ignore //bits.wikimedia.org
    only use //upload.wikimedia.org
    
    """
    
    def get_pics(self,soup):
        pic_list = list()
        
        """ add only images themselves to list """
        for image in soup.find_all('img'):
            page_url = image.get('src')
            temp_img = Parser(page_url)
            if 'bits.wikimedia.org' in temp_img.page_url:
                continue
            else:
                pic_list.append(temp_img)
            
            for keyword in filtered_keywords:
                for item in pic_list:
                    if keyword in item.page_url:
                        pic_list.remove(item)
             
        """ print image links """     
        for item in pic_list:
            print item.page_url

   
  

