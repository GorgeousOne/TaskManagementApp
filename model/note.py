import uuid

from model.event_source import EventSource


class Note(EventSource):
	"""Stores all information about a task."""
	def __init__(self, title, description, date, time=None, project=None):
		super().__init__("on_note_change")
		self.uuid = uuid.uuid4()
		self.title = title
		self.description = description
		self.date = date
		self.time = time
		self.project = project
		self.is_done = False

	def get_title(self):
		return self.title

	def set_title(self, title):
		self.title = title

	def get_description(self):
		return self.description

	def set_description(self, description):
		self.description = description

	def get_date(self):
		return self.date

	def set_date(self, qdate):
		self.date = qdate

	def get_time(self):
		return self.time

	def set_time(self, qtime):
		self.time = qtime

	def get_project(self):
		return self.project

	def set_project(self, project):
		self.project = project

	def get_is_done(self):
		return self.is_done

	def toggle_is_done(self):
		self.is_done = not self.is_done

	def __hash__(self):
		return hash(self.uuid)

	def __eq__(self, other):
		if not isinstance(other, Note):
			return False
		return self.uuid == other.uuid

	def __lt__(self, other):
		"""Compares the time difference between itself and another note"""
		if not isinstance(other, Note):
			return False
		# compare day difference
		if not self.date == other.date:
			return self.date.daysTo(other.date) > 0
		# compares day time difference, notes without a time will be listed in beginning of day
		if self.time:
			return self.time.secsTo(other.time) > 0 if other.time else False
		# sort notes without time alphabetically
		else:
			return True if other.time else self.title == min(self.title, other.title)

	def __repr__(self):
		return f"<Note {str(self.uuid)[-5:]}: {self.title}>"
