from os.path import join, isdir
from os import listdir

from ..core.utils.string import remove_text

class Web_Router:

	routes = {
		'web': {},
		'api': {}
	}

	trigger_files = [
		'page.html',
		'layout.html',
		'api.py',
		'middleware.py'
	]

	def __init__(self, base_path) -> None:
		self.base_path = base_path
		self.find_routes(self.base_path)
		print(self.routes)

	def find_routes(self, search_path):
		for item in self.scan_folder_for_trigger(search_path):
			new_path = join(search_path, item)
			if isdir(new_path):
				self.find_routes(new_path)
			else:
				if item in self.trigger_files:
					protocol = 'web'
					file_path = remove_text(search_path, self.base_path)
					if item == 'api.py':
						protocol = 'api'
						file_path = join('/api', file_path)
					self.routes[protocol][file_path] = new_path

	def scan_folder_for_trigger(self, search_path):
		return listdir(search_path)