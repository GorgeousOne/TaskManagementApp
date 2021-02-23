
class Project:
	def __init__(self, uuid, name, color):
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

	def add_listener(self, listener):
		event_method = getattr(listener, "project_change_event", None)
		if not callable(event_method):
			raise Exception("Could not add listener missing the update_data method")
		self._listeners.append(listener)

	def remove_listener(self, listener):
		self._listeners.remove(listener)

	def update_listeners(self):
		for listener in self._listeners:
			listener.project_change_event(self)

	def __getstate__(self):
		"""Removes the temporary listeners from the data to pickle"""
		state = self.__dict__.copy()
		del state['_listeners']
		return state

	def __setstate__(self, state):
		"""Ensures listeners not to be None after unpickeling"""
		self.__dict__.update(state)
		self._listeners = []

	def __lt__(self, other):
		if not isinstance(other, Project):
			return False
		return self.name < other.name
