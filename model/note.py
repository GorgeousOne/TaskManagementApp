
class Note:
	def __init__(self, title, date, description="", time=None, priority=""):
		self.title = title
		self.date = date
		self.time = time
		self.description = description
		self.isDone = False

	def __hash__(self):
		return hash((self.title, self.date))

	def __eq__(self, other):
		if not isinstance(other, Note):
			return False

		if self.title == other.title and self.date == other.date:
			return self.time == other.time
		return False

	def __repr__(self):
		return f"<Note: {self.title}>"
