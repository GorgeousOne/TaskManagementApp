from model.event_source import EventSource


class Project(EventSource):
	"""Stores all information about a project."""
	def __init__(self, uuid, name, color):
		super().__init__("on_project_change")
		self.uuid = uuid
		self.name = name
		self.color = color
		self._listeners = []

	def get_name(self):
		return self.name

	def get_color(self):
		return self.color

	def set_name(self, name):
		self.name = name

	def set_color(self, color):
		self.color = color

	def __getstate__(self):
		"""Removes the listeners bound to the running session from the data to dump"""
		state = self.__dict__.copy()
		del state['_listeners']
		return state

	def __setstate__(self, state):
		self.__dict__.update(state)
		self._listeners = []

	def __eq__(self, other):
		if not isinstance(other, Project):
			return False
		return self.uuid == other.uuid

	def __lt__(self, other):
		if not isinstance(other, Project):
			return False
		return self.name < other.name

	def __repr__(self):
		return f"<Note {str(self.uuid)[-5:]}: {self.name}>"
