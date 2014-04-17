# controller.py

from network.network import NetworkRequest
import model.model as mod
import common.singleton as singleton




class Controller():


    def __init__(self, creation_callback):
        self.model = mod.Model()
        self.requests = [] #holds network request objects

        print creation_callback
        self.node_creation_callback =  creation_callback

    def create_node(self, issued_request, keyword):

        nr = NetworkRequest(issued_request, self.on_search_success)
        nr.get_page(keyword)
        self.requests.append(nr)

    def on_search_success(self, completed_request, model_node):
        if not model_node:
            return
        self.node_creation_callback(model_node)
        self.requests.remove(completed_request) #network request completed so remove

    def get_related_nodes(self, keyword):
        pass

    def find_event_handler(self, touch, function):
        model_node= self.model.find_event_handler(touch)
        if not model_node:
            return False
        node = model_node.get_ui_reference()
        text = model_node.get_text()
        source = model_node.get_source()

        if function == 'on_touch_up':
            if node.user_wants_summary():
                self.create_node(model_node, model_node.get_keyword())
            return node.on_touch_up(touch, text, source)
        elif function == "on_touch_down":
            return node.on_touch_down(touch)
        elif function == 'on_touch_move':
            return node.on_touch_move(touch)
        else:
            return False


