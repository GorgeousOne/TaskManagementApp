import bisect
from PySide2 import QtWidgets
from PySide2.QtCore import Qt

from uis.ui_task_item import UiTaskItem


class UiDateSection(QtWidgets.QWidget):
	"""A widget for displaying all task items of one day together with a date as header"""
	def __init__(self, date):
		super().__init__()
		self.date = date
		self.task_items = []
		self.visible_item_count = 0

		self.vertical_layout = QtWidgets.QVBoxLayout(self)
		self.vertical_layout.setContentsMargins(0, 0, 0, 0)

		# creates the header
		self.date_label = QtWidgets.QLabel(self)
		self.date_label.setMaximumHeight(20)
		self.date_label.setText(self.date.toString("dddd, d. MMMM yy"))
		self.date_label.setStyleSheet("font: 8pt \"Segoe UI\";")
		self.vertical_layout.addWidget(self.date_label, 0, Qt.AlignHCenter)

		# creates the dividing line
		self.line = QtWidgets.QFrame(self)
		self.line.setFrameShape(QtWidgets.QFrame.HLine)
		self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
		self.vertical_layout.addWidget(self.line)

		# creates the area for the tasks to be displayed
		self.task_area = QtWidgets.QWidget(self)
		self.vertical_layout.addWidget(self.task_area)

		self.vertical_layout_2 = QtWidgets.QVBoxLayout(self.task_area)
		self.vertical_layout_2.setContentsMargins(10, 10, 10, 10)
		self.vertical_layout_2.setSpacing(10)

	def task_count(self):
		"""Returns the amount of tasks listed in this section"""
		return len(self.task_items)

	def any_tasks_are_visible(self):
		"""Returns if any of the tasks inside this section are visible with the currently applied project filter"""
		for task in self.task_items:
			if task.isVisible():
				return True
		return False

	def display_task(self, new_task):
		"""Creates a task item for the task and displays adds it to the layout"""
		new_item = UiTaskItem(new_task, self)
		index = bisect.bisect_right(self.task_items, new_item)

		self.task_area.layout().insertWidget(index, new_item)
		self.task_items.insert(index, new_item)
		self.visible_item_count += 1
		return new_item

	def set_item_visible(self, item, is_visible):
		"""Sets visibility of an item and hides the section itself if no items are visible in it"""
		if self.visible_item_count == 0 and is_visible:
			self.show()

		item.setVisible(is_visible)
		self.visible_item_count += 1 if is_visible else -1

		if self.visible_item_count == 0:
			self.hide()

	def update_item(self, task):
		"""Updates the time/alphabet related position of an item inside this section after being changed"""
		item = self.get_item(task)
		self.task_items.remove(item)
		new_index = bisect.bisect_right(self.task_items, item)
		self.task_area.layout().insertWidget(new_index, item)
		self.task_items.insert(new_index, item)

	def remove_task(self, task):
		item = self.get_item(task)
		item.hide()
		item.deleteLater()
		self.task_items.remove(item)
		task.remove_listener(item)
		return

	def get_item(self, task):
		"""Returns the task item from this section associated with the given task"""
		for item in self.task_items:
			if item.task == task:
				return item
		raise Exception(str(task) + " not listed in " + self.date.toString("d. MMMM yy"))

	def __lt__(self, other):
		if not isinstance(other, UiDateSection):
			return False
		return self.date < other.date
