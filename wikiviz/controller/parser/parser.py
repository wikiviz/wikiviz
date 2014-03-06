"""@package parser
Main Parser Module. 

Translates keywords into related links, images, and text.
"""

from bs4 import BeautifulSoup
from types import NoneType
from collections import Counter

filtered_keywords = ('Help:', 'Category:', 'Talk:', 'Special:', 'Wikipedia:', 'bits.wikimedia.org', 'File:', 'en/thumb/', '.svg.', 'Portal:', 'Template:', 'Template_', '/Main_Page')

class Parser(object):

    
    """ @class parser
        Main parser class description """
    class PageLink():

        def __init__(self, page_url, page_name = None, page_priority = 10, occur_count = 0):

            self.page_url = page_url
            self.page_name = page_name
            self.page_priority = page_priority
            self.occur_count = occur_count

        
    def __init__(self, page_url = None, page_name = None, page_priority = 10, occur_count = 0):

        self.page_url = page_url
        self.page_name = page_name
        self.page_priority = page_priority
        self.occur_count = occur_count
        
    
    """ 
    function definitions
    
    """
    
    """
    get links
    page and image links are currently separate
    """
    
    def get_links(self, soup):
        
        link_list = list()
        pic_list = list()
               
        """ get links from wiki article that have a type and are NOT anchors """
        for anchor in soup.find_all('a'):
            page_url = anchor.get('href')
            
            """ initially set priority to 10, just for starters"""
            temp_link = Parser(page_url)
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
        
        return link_list
    
    """ noch to remove:
    Category:
    Main_page
    Portal:
    Wikipedia:
    Special:
    """

        
            
    """
    get word alone
    
    """
    def get_link_word(self, link_list):

        link_word_list = list()
       
        ###need to change object's attribute, NOT start new list...
        for word in link_list:
            word.page_name = word.page_url[6:]
    
            
        """filter out symbols in words"""
        for word in link_list:
            if('_' in word.page_name or '#' in word.page_name):
                
                word.page_name = word.page_name.replace("_", " ")
                head, sep, tail = word.page_name.partition('#')
                word.page_name = head
                
            if('(' in word.page_url):
                head, sep, tail = word.page_name.partition('(')
                word.page_name = head
##                
####            #####convert UTF-8 to ascii!!
        
        return(link_list)


    """
    prioritize links

    TODO:
    -multiple functions?
    -how to send this to model?
    
    """
    def prioritize_links(self, link_list,search_term):

        link_name_list = list()
        distinct_link_list = list(set(link_list))
        num_occur = list()

        occur_sum = 0
        occur_average = 0

        """add priority points if search term in the page name"""
        ##make case insensitive
        for word in link_list:
            if(search_term in word.page_name):
                word.page_priority += 10

        """make list of page names for processing"""
        for word in link_list:
            link_name_list.append(word.page_name)

        """count occurences of each page name in list"""
        for word in link_list:
            counter = link_name_list.count(word.page_name)
            word.occur_count = counter

        """create list of counts for averaging"""
        for word in link_list:
            num_occur.append(word.occur_count)

        """get average num of occurences of each page name"""
        for n in num_occur:
            occur_sum = occur_sum + n
            
        average = occur_sum/len(num_occur)

        """change priority according to average num of occurences """
        for word in link_list:
            if(word.occur_count > average):
                word.page_priority += 4
            elif(word.occur_count < average):
                word.page_priority -= 4
                
        """ print priority """
        for word in distinct_link_list:
            print word.page_name + ": " + str(word.page_priority)
            

       
 
            ###to extract sentences, prob need NLTK"""
    """
    get images: 
    ignore //bits.wikimedia.org
    only use //upload.wikimedia.org
    
    """
##    
##    def get_pics(self,soup):
##        pic_list = list()
##        
##        add only images themselves to list 
##               get images: ignore //bits.wikimedia.org, only use //upload.wikimedia.org 
##        for image in soup.find_all('img'):
##            image_url = image.get('src')
##            temp_img = Parser()
##            if type(temp_link.page_url) is not NoneType and temp_link.page_url.startswith('/wiki/'):
##            
##                continue
##            else:
##                pic_list.append(temp_img)
##            
##            for keyword in filtered_keywords:
##                for item in pic_list:
##                    if keyword in item.page_url:
##                        pic_list.remove(item)
##             
##        """ print image links """     
##        for item in pic_list:
##            print item.image_url
##
##   
##  

