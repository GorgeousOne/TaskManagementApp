import uuid

from PySide2 import QtGui

from model.event_source import EventSource


class Project(EventSource):
	"""Stores all information about a project."""
	def __init__(self, name, color=QtGui.QColor(63, 81, 181)):
		super().__init__("on_project_change")
		self.uuid = uuid.uuid4()
		self.name = name
		self.color = color
		self.listeners = []

	def get_name(self):
		return self.name

	def get_color(self):
		return self.color

	def set_name(self, name):
		self.name = name

	def set_color(self, color):
		self.color = color

	def __eq__(self, other):
		if not isinstance(other, Project):
			return False
		return self.uuid == other.uuid

	def __lt__(self, other):
		if not isinstance(other, Project):
			return False
		return self.name < other.name

	def __repr__(self):
		return f"<Project {str(self.uuid)[-5:]}: {self.name}>"
