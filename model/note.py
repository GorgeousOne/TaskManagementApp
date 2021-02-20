
class Note:
	def __init__(self, uuid, title, date, description="", time=None, priority=""):
		self.uuid = uuid
		self.title = title
		self.date = date
		self.time = time
		self.description = description
		self.is_done = False
		self._listeners = []

	def add_listener(self, listener):
		update_method = getattr(listener, "update_data", None)
		if not callable(update_method):
			raise Exception("Could not add listener to note missing the update_data method")
		self._listeners.append(listener)

	def remove_listener(self, listener):
		self._listeners.remove(listener)

	def update_listeners(self):
		for listener in self._listeners:
			listener.update_data()

	def get_is_done(self):
		return self.is_done

	def toggle_is_done(self):
		self.is_done = not self.is_done

	def __getstate__(self):
		"""Removes the temporary listeners from the data to pickle"""
		state = self.__dict__.copy()
		del state['_listeners']
		return state

	def __setstate__(self, state):
		"""Ensures listeners not to be None after unpickeling"""
		self.__dict__.update(state)
		self._listeners = []

	def __hash__(self):
		return hash(self.uuid)

	def __eq__(self, other):
		if not isinstance(other, Note):
			return False
		return self.uuid == other.uuid

	def __lt__(self, other):
		if not isinstance(other, Note):
			return False

		if not self.date == other.date:
			return self.date.daysTo(other.date) > 0
		if not self.time:
			return True
		if not other.time:
			return False
		return self.time.secsTo(other.time) > 0

	def __repr__(self):
		return f"<Note: {self.title}>"
