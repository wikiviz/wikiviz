"""@module network
Main Network Module. 

Retrieves data from wikipedia.
"""

from kivy.network.urlrequest import UrlRequest
import urllib

class Singleton(type):
    """ using the metaclass approach to singleton in python:
        http://stackoverflow.com/questions/31875/is-there-a-simple-elegant-way-to-define-singletons-in-python/33201#33201
    """
    def __init__(cls, name, bases, dict):
        super(Singleton, cls).__init__(name, bases, dict)
        cls.instance = None 

    def __call__(cls,*args,**kw):
        if cls.instance is None:
            cls.instance = super(Singleton, cls).__call__(*args, **kw)
        return cls.instance


class Network(object):
    """ Retrieve raw data from Wikipedia, return as page data """    
    __metaclass__ = Singleton
    
    def __init__(self):
        # play nice with the Wikipedia API:
        self.headers = {'User-Agent': 'Wikiviz/0.1 (https://github.com/wikiviz/wikiviz; anrevl01@louisville.edu) Educational Use', 
                            'Content-type': 'application/json',
                            'Accept': 'text/plain' }

    def on_success(self, request, result):
        print "Success!"
        print result

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
