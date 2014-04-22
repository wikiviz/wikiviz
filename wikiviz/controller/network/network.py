# -*- coding: utf-8 -*-
""" utf coding required to deal with html data """

"""@module network
Main Network Module. 

Retrieves data from wikipedia.
"""


from kivy.network.urlrequest import UrlRequest
import urllib
import model.model as mod
import re
from kivy.event import EventDispatcher
import sys

import controller.parser.parser as parser
from bs4 import BeautifulSoup

class NetworkRequest(EventDispatcher):
    """
    Retrieves raw data from Wikipedia based on keyword or URL,
    parses results and adds Nodes to Model
    """

    def __init__(self, issued_request, callback):
        # play nice with the Wikipedia API:
        self.headers = {'User-Agent': 'Wikiviz/0.1 (https://github.com/wikiviz/wikiviz; anrevl01@louisville.edu) Educational Use', 
                            'Content-type': 'application/json',
                            'Accept': 'text/plain' }

        self.issued_request = issued_request # reference to parent model node
        self.model = mod.Model()
        self.callback = callback # controller routine to handle completed requests
        self.keyword = None

        self.register_event_type("on_get_page_by_keyword")
        self.register_event_type("on_get_page_by_url")

    def on_get_page_by_keyword(self, keyword):
        """
            First request is user inputted keyword.
            We have to retrieve the url of the page by searching wikipedia
        """
        # sanitize keyword
        if self.model.has_been_explored_yet(keyword):
            return;

        self.keyword = keyword
        keyword = urllib.quote(keyword)
        print "keyword encoded: ", keyword

        # search wikipedia for keyword
        url = "http://en.wikipedia.org/w/api.php?action=query&format=json&srprop=timestamp&list=search&srsearch=" + keyword
        print "Searching wikipedia for", keyword, ": ", url
        req = UrlRequest(url=url, on_success=self.on_search_success, on_error=self.on_error, req_headers=self.headers, decode=True)

        
    def on_search_success(self, request, result):
        """
        Called when keyword search returns data.
        Picks top search result and fetches its page content
        """
        try:
            results = result['query']['search']
        except:
            return self.on_error(request, "no results found")

        # pick top result
        top_result = urllib.quote( results[0]['title'].encode("utf8") )

        # fetch page content from url
        url = "http://en.wikipedia.org/w/api.php?format=json&action=query&prop=revisions&rvprop=content&rvparse=1&titles=" + top_result
        self.on_get_page_by_url(url)


    def on_get_page_by_url(self, url):
        """
        Called when we already know the url of the node we want to create.
        Used for keyword and child nodes
        """        
        print "Retrieving page data from", url
        req = UrlRequest(url=url, on_success=self.on_success, on_error=self.on_error, req_headers=self.headers, decode=True)


    def on_success(self, request, result):
        """
        Called when UrlRequest returns with page data for keyword
        Takes raw page data, runs through parser, creates model node
        """
        print "Page successfully retrieved from Wikipedia, request:", request
        page_content = ""
        page_title = ""
        
        try:
            # wiki api returns json object
            pages = result['query']['pages']

            # page data is stored by key; key =page id
            for key, value in pages.items():
                print "Page id:", key
                page_content = value["revisions"][0]["*"]
                page_title = value["title"]
        except TypeError:
            # if result is not in json format a type error occurs and 
            # that means get_page_by_url is calling and the result is plain HTML
            print "Non-API page returned"            
            soup = BeautifulSoup(result)            
            page_content = soup.body.get_text()
            page_title = soup.title.get_text()
            page_title = page_title.replace(" - Wikipedia, the free encyclopedia", "")

        except:
            # something else went wrong
            print "An error occurred while processing the request result"
            print "request: ", request
            # print "result: ", result
            print "Unexpected error:", sys.exc_info()[0]
            self.on_error(request, None)
            return
        
        if page_content == None or page_title == None:
            print "no page or title content"
            self.on_error(request, None)     
            return           
        
        p = parser.Parser(page_content)
        page_links = p.get_links(5)
        page_images = p.get_images(5)
        
        #everett added re because the link doesn't resturn results in ****result['query']****** format
        # links = []
        # for eachPageLink in page_links:
        #     child_keyword = re.search(u'[0-9A-Za-z]*$', eachPageLink)
        #     links.append(child_keyword.group(0))

        # page_links = links
        print "page_links:", page_links
        print "page_images:", page_images

        ##################################################
        #the page summary from parser goes in page_summary
        page_summary = self.keyword
        ##################################################

        node = mod.Node(self.issued_request, page_title, request.url, page_images, page_summary, page_content, page_links, False)
        #def __init__(self, parent, keyword, href, img_src, summary, page_content, links, has_visited=False):
        node.set_id(node)
        self.model.add_node(node)
        self.callback(self, node)
    
    def on_error(self, request, error):
        self.callback(self, False)
        print "Error during network request!"
        print error
