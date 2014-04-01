"""@package parser
Main Parser Module.

Translates keywords into related links, images, and text.
"""

from bs4 import BeautifulSoup
from types import NoneType
import re
import strip_tags


import summarizer

filtered_keywords = ('Help:', 'Category:', 'Talk:', 'Special:', 'Wikipedia:', 'bits.wikimedia.org', 'File:',
                     'en/thumb/', '.svg.', 'Portal:', 'Template:', 'Template_', '/Main_Page')

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

    def __init__(self, raw_page_content, link_list = list(), image_list = list()):

        self.soup = BeautifulSoup(raw_page_content)
        self.link_list = link_list
        self.image_list = image_list

    def extract_links(self):

        """ get links from wiki article that have a type and are NOT anchors """
        #link_list = list()

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
                    if keyword in item.page_url:
                        self.link_list.remove(item)

        return self.link_list


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
            for item in image_list:
                if keyword in item.page_url:
                    image_list.remove(item)

        return image_list

    def get_links(self):

        return self.link_list

    def get_images(self):

        return self.image_list


    #how to send this to model?
    @staticmethod
    def prioritize_links(self, search_term):


        link_name_list = list()

        num_occur = list()

        occur_sum = 0

        #add priority points if search term in the page name
        ##make case insensitive
        for word in self.link_list:
            if search_term in word.page_name:
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

        #change priority according to average num of occurrences """
        for word in self.link_list:
            if word.occur_count > average:
                word.page_priority += 4
            elif word.occur_count < average:
                word.page_priority -= 4

        return self.link_list


    @staticmethod
    def remove_duplicates(p_link_list):

        new_set = set()
        distinct_link_list = []
        for item in p_link_list:
            if item.page_name not in new_set:
                distinct_link_list.append(item)
                new_set.add(item.page_name)

        #second filter run through, shouldn't have to do this, still doesn't filter all!!
        for keyword in filtered_keywords:
                for item in distinct_link_list:
                    if keyword in item.page_url:
                        if keyword in item.page_url:
                            distinct_link_list.remove(item)

        return distinct_link_list


    ###to extract sentences, prob need NLTK


    def get_text_summary(self):

        paragraphs = self.soup.find_all("p", limit=3)
        soup_string = ""

        for item in paragraphs:
            item = str(item)
            item = re.sub('<[^<]+?>', '', item)

            #i know we had talked about not using concatenation, but i'm having trouble with join() at the moment
            soup_string += (item + '\n\n')
        print soup_string



