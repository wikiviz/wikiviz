# controller.py


import model.model as mod
from network.network import NetworkRequest
from kivy.clock import Clock



class Controller(object):


    def __init__(self, node_creation_callback, red_edge_creation_callback, edge_creation_callback):
        self.model = mod.Model(self.node_creation, self.edge_creation)
        self.requests = [] #holds network request objects
        self.model = mod.Model()

        self.node_creation_callback =  node_creation_callback
        self.red_edge_creation_callback = red_edge_creation_callback
        self.edge_creation_callback = edge_creation_callback


    def find_event_handler(self, touch, function):
        model_node= self.model.find_event_handler(touch)
        if not model_node:
            return False
        node = model_node.get_ui_reference()

        if function == 'on_touch_up':
            return node.on_touch_up(touch)
        elif function == "on_touch_down":
            return node.on_touch_down(touch)
        elif function == 'on_touch_move':
            return node.on_touch_move(touch)
        else:
            return False

    def dump_nodes(self):
        self.model.dump_nodes()
    def dump_edges(self):
        self.model.dump_edges()

    def get_edges(self):
        return self.model.get_edges()

    def node_creation(self, node):
        self.node_creation_callback(node)
    def edge_creation(self, par, child):
        self.edge_creation_callback(par,child)
    def red_edge_creation(self, child):
        self.red_edge_creation_callback(child)

class NetworkController(Controller):
    def __init__(self, *args, **kwargs):
        self.pending_requests = []
        self.requests = []
        super(NetworkController, self).__init__(*args,**kwargs)
    def search_by_keyword(self, issued_request, keyword):

        # this is the root node
        nr = NetworkRequest(issued_request, self.root_creation_callback)
        nr.on_get_page_by_keyword(keyword)
        self.requests.append(nr)

    def search_by_url(self, model_node):
        if self.pending_requests == []:
            Clock.schedule_interval(self.handle_get_page_by_url_requests, 3.)
        for eachKeyword in model_node.links.keys():
            nr = NetworkRequest(model_node, self.on_success, model_node.get_keyword())
            print eachKeyword
            self.pending_requests.append((nr, model_node.links[eachKeyword]))

    def on_success(self, completed_request, model_node):
        # called when child nodes are loaded
        self.requests.remove(completed_request) # network request completed so remove
        if not model_node:
            return
        self.node_creation(model_node)
        self.edge_creation(model_node.get_parent_ui_reference(),model_node.get_ui_reference())

    def handle_get_page_by_url_requests(self, *args):
        print "Args",args
        if self.pending_requests:
            nr, url = self.pending_requests.pop()
            nr.on_get_page_by_url(url)
            self.requests.append(nr)
        else:
            Clock.unschedule(self.handle_get_page_by_url_requests)
        return

    def root_creation_callback(self, completed_request, model_node):
        if not model_node:
            print "No Root Model Node"
            assert(False)
        self.requests.remove(completed_request) #network request completed so remove
        #model_node.has_visited = True
        #Clock.schedule_interval(self.handle_get_page_by_url_requests, 3.)
        print model_node
        #self.search_by_url(model_node)
        self.node_creation(model_node)


    def find_event_handler(self, touch, function):
        model_node= self.model.find_event_handler(touch)
        if not model_node:
            return False
        node = model_node.get_ui_reference()
        text = model_node.get_summary()
        source = model_node.get_source()
        print text
        print source
        if function == 'on_touch_up':
            if node.user_wants_summary() and not model_node.has_visited:
                self.red_edge_creation(model_node)
                self.search_by_url(model_node)
                model_node.has_visited = True
                return node.on_touch_up(touch)
            elif not node.user_wants_summary():
                return node.on_touch_up(touch)
            return node.on_touch_up(touch, text, source)
        elif function == "on_touch_down":
            return node.on_touch_down(touch)
        elif function == 'on_touch_move':
            return node.on_touch_move(touch)
        else:
            return False

    def dump_nodes(self):
        self.model.dump_nodes()