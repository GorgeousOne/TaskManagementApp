import bisect

from PySide2 import QtCore

from uis.ui_project_item import UiProjectItem


class UiProjectBar:
	def __init__(self, container):
		self.container = container
		self.layout = container.layout
		self.projects = []

	def add_project(self, new_project):
		index = bisect.bisect_right(self.projects, new_project)
		new_item = UiProjectItem(new_project, self)

		# self.projects.insert(index, new_time)
		# self.note_area.layout().insertWidget(index, new_item)
		# self.items.insert(index, new_item)
		return new_item
