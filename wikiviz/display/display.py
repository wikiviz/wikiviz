"""@package display
Main Display Module. 

Any supplementary display code
"""
import wikiviz.model as mod



class Display():
    """ @class display 
    Main Display class """

    def __init__(self):
        """ The constructor
        @param self default parameter for constructor """
        self.model = mod.model.Model()
        print "Display created"

    def trigger_update(self):
        print "display is updating!"
        if len(self.model.nodes) > 3:
            self.model.print_graph()