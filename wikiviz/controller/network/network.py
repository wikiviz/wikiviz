"""@module network
Main Network Module. 

Retrieves data from wikipedia.
"""

from kivy.network.urlrequest import UrlRequest
import urllib
import model.model as mod
import common.singleton as singleton

class Network(object):
    """ Retrieve raw data from Wikipedia, return as page data """    
    __metaclass__ = singleton.Singleton
    
    def __init__(self):
        # play nice with the Wikipedia API:
        self.headers = {'User-Agent': 'Wikiviz/0.1 (https://github.com/wikiviz/wikiviz; anrevl01@louisville.edu) Educational Use', 
                            'Content-type': 'application/json',
                            'Accept': 'text/plain' }

    def on_success(self, request, result):
        print "Success!"
        print result

        model = mod.Model()
        print model
        
        node = mod.Node("kw", "href", "imgsrc", "text", "links", False)
        print node
        
        model.add_node(node)
        print "added node"

        model.print_graph()


    def on_error(self, request, error):
        print "Error!"
        print error

    def get_page(self, keyword):
        try: 
            keyword = urllib.urlencode(keyword)
        except TypeError:
            pass

        url = "http://en.wikipedia.org/w/api.php?action=parse&format=json&title=" + keyword
        req = UrlRequest(url=url, on_success=self.on_success, on_error=self.on_error, req_headers=self.headers, decode=False)