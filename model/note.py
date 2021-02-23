from model.event_source import EventSource


class Note(EventSource):
	def __init__(self, uuid, title, date, description="", time=None, project=None):
		super().__init__("on_note_change")
		self.uuid = uuid
		self.title = title
		self.description = description
		self.date = date
		self.time = time
		self.project = project
		self.is_done = False

	def get_is_done(self):
		return self.is_done

	def toggle_is_done(self):
		self.is_done = not self.is_done

	def __getstate__(self):
		"""Removes the temporary listeners from the data to pickle"""
		state = self.__dict__.copy()
		del state["_event_method_name"]
		del state["_listeners"]
		return state

	def __setstate__(self, state):
		"""Ensures listeners not to be None after unpickeling"""
		self.__dict__.update(state)
		self._event_method_name = "on_note_change"
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
		return f"<Note {str(self.uuid)[-5:]}: {self.title}>"
