# -*- coding: utf-8 -*-
""" utf coding required to deal with html data """

"""@module network
Main Network Module. 

Retrieves data from wikipedia.
"""


from kivy.network.urlrequest import UrlRequest
import urllib
import wikiviz.model.model as mod

import wikiviz.controller.parser.parser as parser
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
        self.callback = callback #controller routine to handle compeleted requests


    def get_page(self, keyword):
        # sanitize keyword
        keyword = urllib.quote(keyword)
        print "keyword encoded: ", keyword

        # search wikipedia first to get the wiki page title
        print "Searching wikipedia for", keyword
        url = "http://en.wikipedia.org/w/api.php?action=query&format=json&srprop=timestamp&list=search&srsearch=" + keyword
        req = UrlRequest(url=url, on_success=self.on_search_success, on_error=self.on_error, req_headers=self.headers, decode=True)


    def on_search_success(self, request, result):
        # parse returned results, pick top one, fetch its page content
        try:
            results = result['query']['search']
        except:
            return self.on_error(request, "no results found")

        top_result = urllib.quote(results[0]['title'])
        url = "http://en.wikipedia.org/w/api.php?format=json&action=query&prop=revisions&rvprop=content&rvparse=1&titles=" + top_result
        print "Retrieving page data for", top_result
        req = UrlRequest(url=url, on_success=self.on_success, on_error=self.on_error, req_headers=self.headers, decode=True)


    def on_success(self, request, result):
        """
        Called when UrlRequest returns with page data for keyword
        Takes raw page data, runs through parser, then stores in model.
        """
        print "Page retrieved from Wikipedia"

        page_content = ""
        page_title = ""

        try:
            pages = result["query"]["pages"]
        except TypeError:
            # if result not found in returned result
            print "Error page returned!"
            self.on_error(None, None)
            return

        # page data is stored by key; key =page id
        for key, value in pages.items():
            print "Page id:", key
            page_content = value["revisions"][0]["*"]
            page_title = value["title"]

        # print "Raw page content:"
        # print page_content
        # print "\n"

        # right now the parser doesn't return anything
        p = parser.Parser(page_content)
        page_links = p.get_links()
        page_images = p.get_images()
        print "page_links:", page_links
        print "page_images:", page_images

        node = mod.Node(self.issued_request, request.url, page_images, page_content, page_links, False)
        self.model.add_node(node)
        self.callback(self, node)
    
    def on_error(self, request, error):
        self.callback(self, False)
        print "Error during network request!"
        print error