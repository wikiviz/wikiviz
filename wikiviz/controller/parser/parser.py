"""@package parser
Main Parser Module.

Translates keywords into related links, images, and text.
"""

from bs4 import BeautifulSoup
from types import NoneType
import re


filtered_keywords = ('help:', 'category:', 'talk:', 'special:', 'wikipedia:', 'bits.wikimedia.org', 'file:',
                     'en/thumb/', '.svg.', 'portal:', 'template:', 'template_', '/main_page', 'disambiguation',
                     'enlarge')

#remove this once this is hooked up to the network


class PageLink(object):

    def __init__(self, page_url=None, page_name=None, page_priority=10, occur_count=0):

        self.page_url = page_url
        self.page_name = page_name
        self.page_priority = page_priority
        self.occur_count = occur_count


class Parser(object):

    """
function definitions
"""

    def __init__(self, raw_page_content, link_list=list(), image_list=list(), high_priority_list=list(),
                 text_summary=None):

        self.soup = BeautifulSoup(raw_page_content)
        self.link_list = link_list
        self.image_list = image_list
        self.high_priority_list = high_priority_list
        self.text_summary = text_summary

    def extract_links(self):

        # get links from wiki article that have a type and are NOT anchors

        for anchor in self.soup.find_all('a'):
            link = anchor.get('href')

            if type(link) is not NoneType and link.startswith("/wiki"):
                if anchor.get('title') is not None:
                    page_url = link
                    page_name = anchor.get('title')
                    temp_link = PageLink(page_url, page_name)
                    self.link_list.append(temp_link)


        #use keywords list to filter out undesirable elements

        for keyword in filtered_keywords:
                for item in self.link_list:
                    if keyword in item.page_url.lower() or keyword in item.page_name.lower():
                        print item.page_url + ": bad word"
                        self.link_list.remove(item)
        print "*******************************"

        for item in self.link_list:
            print item.page_url


    def extract_images(self):

        image_list = list()

        #get images, filter
        for image in self.soup.find_all('img'):
            page_url = image.get('src')
            temp_img = PageLink(page_url)
            if type(temp_img.page_url) is not NoneType and temp_img.page_url.startswith('/wiki/'):
                continue
            else:
                image_list.append(temp_img)

        for keyword in filtered_keywords:
                for item in self.image_list:
                    if keyword in item.page_url:
                        self.link_list.remove(item)

    def get_links(self):

        return self.link_list

    def get_images(self):

        return self.image_list

    # sets priorities for all links, then creates a link of the highest priority items
    # returns whole list and high priority list
    @staticmethod
    def prioritize_links(self, search_term):

        link_name_list = list()

        num_occur = list()

        occur_sum = 0

        #add priority points if search term in the page name
        for word in self.link_list:
            lower_page_name = word.page_name.lower()
            if search_term in lower_page_name:
                word.page_priority += 10

        #make list of page names for processing
        for word in self.link_list:
            link_name_list.append(word.page_name)

        #count occurrences of each page name in list
        for word in self.link_list:
            counter = link_name_list.count(word.page_name)
            word.occur_count = counter

        #create list of counts for averaging
        for word in self.link_list:
            num_occur.append(word.occur_count)

        #get average num of occurrences of each page name
        for n in num_occur:
            occur_sum = occur_sum + n

        average = occur_sum / len(num_occur)

        #change priority according to average num of occurrences
        for word in self.link_list:
            if word.occur_count > average:
                word.page_priority += 4
            elif word.occur_count < average:
                word.page_priority -= 4

        #create distinct link list
        new_set = set()
        distinct_link_list = []
        for item in self.link_list:
            if item.page_name not in new_set:
                distinct_link_list.append(item)
                new_set.add(item.page_name)

        self.link_list = distinct_link_list

        #create list of highest priority items, with a max of 10
        for item in self.link_list:
            if item.page_priority > 10:
                if len(self.high_priority_list) <= 10:
                    self.high_priority_list.append(item)


    #make filtered keyword lists here
    def get_text_summary(self):

        div = self.soup.find("div", attrs={"id": "mw-content-text"})
        self.text_summary = ""

        for item in div.contents:
            if "<p>" in unicode(item) or "<li>" in unicode(item):
                item = unicode(item)
                item = re.sub('<[^<]+?>', '', item)
                self.text_summary += item + "\n\n"
            if "<h2>" in unicode(item):
                break


