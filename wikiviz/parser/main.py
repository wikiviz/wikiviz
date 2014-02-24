"""@package parser

Text Parser
"""


from bs4 import BeautifulSoup
from bs4 import SoupStrainer
from types import NoneType

filtered_keywords = ('Help:', 'Category:', 'Talk:', 'Special:', 'Wikipedia:', 'File:', 'en/thumb/', '.svg.')

""" function definitions """

""" class definition """

class PageLink:
    
    def __init__(self, page_url, page_priority):
        self.page_url = page_url
        self.page_priority = page_priority
        
class ImageLink:
    
    def __init__(self, image_url, image_priority):
        self.image_url = image_url
        self.image_priority = image_priority        
        
        
"""
get links
"""

"""
currently, page and image links are separate
"""

def get_links(soup):
    
    link_list = list()
    
    """ use keywords list to filter out undesirable elements"""
    
    
    """ get links from wiki article that have a type and are NOT anchors """
    for anchor in soup.find_all('a'):
        page_url = anchor.get('href')
        
        """ initially set priority to 3, just for starters"""
        temp_link = PageLink(page_url,3)
        if type(temp_link.page_url) is not NoneType and temp_link.page_url.startswith('/wiki/'):
            link_list.append(temp_link)
    
        for keyword in filtered_keywords:
            for item in link_list:
                if keyword in item.page_url:
                    link_list.remove(item)
    
    """create distinct set of links"""
    distinct_link_list = list(set(link_list))
    
    """ print list """
    for elem in distinct_link_list:
        print elem.page_url
        
        
"""
get images: 
ignore //bits.wikimedia.org
only use //upload.wikimedia.org

"""
def get_pics(soup):
    pic_list = list()
    
    """ add only images themselves to list """
    for image in soup.find_all('img'):
        image_url = image.get('src')
        temp_img = ImageLink(image_url, 3)
        if 'bits.wikimedia.org' in temp_img.image_url:
            continue
        else:
            pic_list.append(temp_img)
        
        for keyword in filtered_keywords:
            for item in pic_list:
                if keyword in item.image_url:
                    pic_list.remove(item)
         
    """ print image links """     
    for item in pic_list:
        print item.image_url

