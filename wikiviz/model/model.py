# model.py
import wikiviz.common.singleton as singleton

class Node():
	def __init__(self, keyword, href, img_src, text, links, has_visited=False):
		self.keyword = keyword 
		self.href = href
		self.img_src = img_src
		self.text = text
		self.links = links
		self.has_visited = has_visited

class Edge():
	def __init__(self, source, destination):
		self.source = source
		self.destination = destination

class Model():
	__metaclass__ = singleton.Singleton
	def __init__(self):
		self.nodes = []
		self.edges = []

	def add_node(self, node):
		self.nodes.append(node)

	def add_edge(self, edge):
		self.edges.append(edge)

	def print_graph(self):
		print "Printing graph in model"
		for n in self.nodes:
			print "Node: ", n
		for e in self.edges:
			print "Edge: ", e