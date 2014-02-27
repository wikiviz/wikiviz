import unittest
import wikiviz.controller.network.network as network


class NetworkTests(unittest.TestCase):
	
	# scaffolding data
	temp_result = "Lorem ipsum dolor sit amet"
	keyword = "Mozart"

	def test_init(self):
		instance = network.Network()
		self.assertTrue(instance)

	def test_on_success(self):
		self.assertTrue(self.temp_result)

	def test_on_error(self):
		pass

	def test_get_instance(self):
		pass

	def test_get_page(self):
		self.assertTrue(self.keyword)
		pass

	
if __name__ == '__main__':
	unittest.main()