
class Note:
	def __init__(self, title, date, description="nothing", priority="so far"):
		self.title = title
		self.date = date
		self.description = description

	def __repr__(self):
		return f"<Note {self.title}>"
