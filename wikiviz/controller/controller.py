# controller.py

from network.network import NetworkRequest
import model.model as mod
import common.singleton as singleton




class Controller():


    def __init__(self, creation_callback):
        self.model = mod.Model()
        self.requests = [] #holds network request objects

        self.node_creation_callback =  creation_callback

    def search_by_keyword(self, issued_request, keyword):

        if issued_request == None:
            nr = NetworkRequest(issued_request, self.root_creation_callback)
            nr.dispatch("on_get_page_by_keyword", keyword)
            self.requests.append(nr)
        else:    
            for eachKeyword in issued_request.links.keys():
                # TODO: should this instead fetch the URL directly
                # with get_page_by_url instead of on_get_page_by_keyword?
                # otherwise the search api is used for all requests
                # search 'turing' to see an example
                nr = NetworkRequest(issued_request, self.on_success)
                print eachKeyword
                nr.dispatch("on_get_page_by_url", issued_request.links[eachKeyword])
                self.requests.append(nr)



    def on_success(self, completed_request, model_node):
        self.requests.remove(completed_request) #network request completed so remove
        if not model_node:
            return
        self.node_creation_callback(model_node)



    def root_creation_callback(self, completed_request, model_node):
        if not model_node:
            print "No Root Model Node"
            assert(False)
        self.requests.remove(completed_request) #network request completed so remove
        for eachKeyword in model_node.links.keys():
            nr = NetworkRequest(model_node, self.on_success)            
            
            nr.dispatch("on_get_page_by_url", model_node.links[eachKeyword])
            self.requests.append(nr)
        self.node_creation_callback(model_node)


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
            if node.user_wants_summary():
                self.search_by_keyword(model_node, model_node.get_keyword())
            return node.on_touch_up(touch, text, source)
        elif function == "on_touch_down":
            return node.on_touch_down(touch)
        elif function == 'on_touch_move':
            return node.on_touch_move(touch)
        else:
            return False

    def dump_nodes(self):
        self.model.dump_nodes()
