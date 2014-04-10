# -*- coding: utf-8 -*-
""" utf coding required to deal with html data """

"""@module network
Main Network Module. 

Retrieves data from wikipedia.
"""


from kivy.network.urlrequest import UrlRequest
import urllib
import model.model as mod

import controller.parser.parser as parser
from bs4 import BeautifulSoup

class NetworkRequest(object):
    """ Retrieve raw data from Wikipedia, return as page data """    
    
    def __init__(self, issued_request, callback):
        # play nice with the Wikipedia API:
        self.headers = {'User-Agent': 'Wikiviz/0.1 (https://github.com/wikiviz/wikiviz; anrevl01@louisville.edu) Educational Use', 
                            'Content-type': 'application/json',
                            'Accept': 'text/plain' }

        self.issued_request = issued_request

        self.model = mod.Model()

        self.callback = callback

    def get_page(self, keyword):
        """
        Gets page from network using kivy's async urlrequest.
        Model notifies Display when update is complete.
        """

        #todo: sanitize input

        print keyword
        keyword = urllib.quote(keyword)
        print "keyword encoded: ", keyword

        # first search wikipedia for the wiki page url
        self.search(keyword)

   
    def search(self, keyword):

        url = "http://en.wikipedia.org/w/api.php?action=query&format=json&srprop=timestamp&list=search&srsearch=" + keyword
        req = UrlRequest(url=url, on_success=self.on_search_success, on_error=self.on_error, req_headers=self.headers, decode=True)

        print 'search'

    
    def on_search_success(self, request, result):
        # parse returned results, pick top one, fetch its page content

 
        results = result['query']['search']
        top_result = results[0]['title']

        top_result = urllib.quote(top_result)
        url = "http://en.wikipedia.org/w/api.php?format=json&action=query&prop=revisions&rvprop=content&rvparse=1&titles=" + top_result
        print "Searching ", url
        req = UrlRequest(url=url, on_success=self.on_success, on_error=self.on_error, req_headers=self.headers, decode=True)



    def on_success(self, request, result):
        """
        Called when UrlRequest returns.
        Takes raw page data, runs through parser, then stores in model.
        """
        print "Success"

        page_content = ""
        page_title = ""

        pages = result["query"]["pages"]

        # page data is stored by key
        for key, value in pages.items():
            # key = page id
            print "Page id:", key
            page_content = value["revisions"][0]["*"]
            page_title = value["title"]

        # TODO: replace BS with parser instance
        soup = BeautifulSoup(page_content, from_encoding="UTF-8")
        # p = parser.Parser(soup)
        # page_links = p.get_links(soup)
        # page_links = p.prioritize_links(page_links, page_title)
        # page_links = p.remove_duplicates(page_links)
        # print page_links
        # page_images = p.get_images()

        page_links = soup.find_all('a')[:5]
        page_images = ""

        node = mod.Node(self.issued_request, request.url, page_images, page_content, page_links, False)
        self.model.add_node(node)
        print "added node ", node
        self.callback(self)
    
    def on_error(self, request, error):
        self.callback(self)
        print "Error!"
        print error
