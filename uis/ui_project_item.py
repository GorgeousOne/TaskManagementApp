from PySide2 import QtWidgets, QtUiTools, QtCore

import utils


class UiProjectItem(QtWidgets.QWidget):
	"""A widget in the sidebar that display a project"""
	def __init__(self, project):
		super().__init__()
		self.project = project
		self.project.add_listener(self)

		self.vertical_layout = QtWidgets.QVBoxLayout(self)
		self.vertical_layout.setContentsMargins(0, 0, 0, 0)

		self.content = QtUiTools.QUiLoader().load("./uis/scripts/ui_project_item.ui")
		self.content.clickable_frame.installEventFilter(self)

		self.vertical_layout.addWidget(self.content)
		self.content.button_bar.hide()
		self.on_project_change(self.project)

		self.click_method = None

	def enterEvent(self, event):
		self.content.button_bar.show()

	def leaveEvent(self, event):
		self.content.button_bar.hide()

	def eventFilter(self, obj, event):
		"""Installs a listener for clicks on the item"""
		if event.type() == QtCore.QEvent.MouseButtonRelease:
			if callable(self.click_method):
				self.click_method()
			return True
		return False

	def on_project_change(self, project):
		"""Updates the displayed data of the project"""
		project_name = self.project.get_name()
		self.content.name_label.setText(project_name)
		self.content.icon_label.setText(project_name[0].upper())

		icon_style = self.content.icon_label.styleSheet()
		icon_style = utils.replace_property(icon_style, "background", self.project.get_color().name())
		self.content.icon_label.setStyleSheet(icon_style)

	def connect_click(self, method):
		"""Sets the method that is being executed when the item is clicked"""
		self.click_method = method

	def __lt__(self, other):
		if not isinstance(other, UiProjectItem):
			return False
		return self.project < other.project
