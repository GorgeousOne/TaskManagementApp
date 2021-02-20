
class Project:
	def __init__(self, uuid, name, color):
		self.uuid = uuid
		self.name = name
		self.color = color

	def get_name(self):
		return self.name

	def get_color(self):
		return self.color

	def __lt__(self, other):
		if not isinstance(other, Project):
			return False
		return self.name < other.name
