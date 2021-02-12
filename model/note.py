
class Note:
	def __init__(self, uuid, title, date, description="", time=None, priority=""):
		self.uui = uuid
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

	def __lt__(self, other):
		if not isinstance(other, Note):
			return False
		day_diff = self.date.daysTo(other.date)
		if day_diff != 0:
			return day_diff < 0
		if self.time:
			return 0
			# return self.time.minutesTo(other.time) < 0 if other.time else True
		return False

	# def __gt__(self, other):
	# 	if not isinstance(other, Note):
	# 		return False
	# 	day_diff = self.date.daysTo(other.date)
	# 	if day_diff != 0:
	# 		return day_diff > 0
	# 	if self.time:
	# 		return self.time.minutesTo(other.time) > 0 if other.time else True
	# 	return False

	def __repr__(self):
		return f"<Note: {self.title}>"
