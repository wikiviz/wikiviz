# controller.py

import display.display as display
import network.network as nw
import model.model as mod
import common.singleton as singleton
import time

class Controller():
	__metaclass__ = singleton.Singleton
	def __init__(self):
		# self.display = display.Display()
		self.network = nw.Network()
		self.model = mod.Model()

	def create_node(self, keyword):
		# the display will sends message that keyword has been entered		
		# get page from network async.
		self.network.get_page(keyword)
		
	def get_related_nodes(self, keyword):
		pass


