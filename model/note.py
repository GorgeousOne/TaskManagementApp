
from datetime import datetime
from dateutil.parser import parse
import json

class Note:
	def __init__(self, title, date, description="nothing", priority="so far"):
		
		self.title = title

		# TODO try catch
		if isinstance(date, datetime):
			self.date = date
		else:
			self.date = parse(date)

		self.description = description


	def __repr__(self):
		return f"<Note {self.title}>"


class NoteEncoder(json.JSONEncoder):
	def default(self, obj):

		if isinstance(obj, Note):
			return {
				"title": obj.title,
				"date": obj.date.strftime("%Y-%m-%d %H:%M"),
				"description": obj.description
			}
		return json.JSONEncoder.default(self, obj)


class NoteDecoder(json.JSONDecoder):
	def __init__(self, *args, **kwargs):
		json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

	
	def object_hook(self, obj):
		return Note(**obj)
