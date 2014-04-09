# controller.py

from network.network import Network
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
        Network.get_page(keyword, self.on_search_success)

    def on_search_success(self, request, result):
        Network.on_search_success(request,result)

    def get_related_nodes(self, keyword):
        pass


