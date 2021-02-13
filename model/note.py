
class Note:
	def __init__(self, uuid, title, date, description="", time=None, priority=""):
		self.uuid = uuid
		self.title = title
		self.date = date
		self.time = time
		self.description = description
		self.isDone = False
		self._listeners = []

	def add_listener(self, listener):
		self._listeners.append(listener)

	def remove_listener(self, listener):
		self._listeners.remove(listener)

	def update_data(self):
		for listener in self._listeners:
			listener.update_data()

	def __getstate__(self):
		# Copy the object's state from self.__dict__ which contains
		# all our instance attributes. Always use the dict.copy()
		# method to avoid modifying the original state.
		state = self.__dict__.copy()
		# Remove the unpicklable entries.
		del state['_listeners']
		return state

	def __setstate__(self, state):
		# Restore instance attributes (i.e., filename and lineno).
		self.__dict__.update(state)
		# Restore the previously opened file's state. To do so, we need to
		# reopen it and read from it until the line count is restored.
		# Finally, save the file.
		self._listeners = []

	def __hash__(self):
		return hash(self.uuid)

	def __eq__(self, other):
		if not isinstance(other, Note):
			return False
		return self.uuid == other.uuid
		# if self.title == other.title and self.date == other.date:
		# 	return self.time == other.time
		# return False

	def __lt__(self, other):
		if not isinstance(other, Note):
			return False
		day_diff = self.date.daysTo(other.date)
		if day_diff != 0:
			return day_diff < 0
		if self.time:
			return 0
		return False

	def __repr__(self):
		return f"<Note: {self.title}>"
