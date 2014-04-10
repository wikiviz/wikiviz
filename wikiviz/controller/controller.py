# controller.py

from network.network import NetworkRequest
import model.model as mod
import common.singleton as singleton




class Controller():
    __metaclass__ = singleton.Singleton

    def __init__(self):
        self.model = mod.Model()
        self.requests = []
    def create_node(self, issued_request, keyword):
        # the display will sends message that keyword has been entered
        # and this function will run, getting page from network async.
        # when get_page is finished, event is passed to display???
        nr = NetworkRequest(issued_request, self.on_search_success)
        nr.get_page(keyword)
        self.requests.append(nr)

    def on_search_success(self, completed_request):
        self.requests.remove(completed_request)

    def get_related_nodes(self, keyword):
        pass

    def find_event_handler(self, touch, function):
        return self.model.find_event_handler(touch, function)

