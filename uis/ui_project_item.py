from PySide2 import QtWidgets, QtUiTools, QtCore

import utils


class UiProjectItem(QtWidgets.QWidget):
	def __init__(self, project, project_bar):
		super().__init__()
		self.project = project
		self.project.add_listener(self)
		self.project_bar = project_bar

		self.verticalLayout = QtWidgets.QVBoxLayout(self)
		self.verticalLayout.setContentsMargins(0, 0, 0, 0)
		#self.setFixedHeight(50)

		self.content = QtUiTools.QUiLoader().load("./uis/res/ui_project_item.ui")
		self.verticalLayout.addWidget(self.content)
		self.content.button_bar.hide()
		self.on_project_change(self.project)

		self.content.clickable_frame.installEventFilter(self)
		self.click_method = None

	def enterEvent(self, event):
		self.content.button_bar.show()

	def leaveEvent(self, event):
		self.content.button_bar.hide()

	def on_project_change(self, project):
		project_name = self.project.get_name()
		self.content.name_label.setText(project_name)
		self.content.icon_label.setText(project_name[0].upper())
		icon_style = utils.replace_property(self.content.icon_label.styleSheet(), "background", self.project.get_color().name())
		self.content.icon_label.setStyleSheet(icon_style)

	def connect_click(self, method):
		self.click_method = method

	def eventFilter(self, obj, event):
		if event.type() == QtCore.QEvent.MouseButtonRelease:
			if callable(self.click_method):
				self.click_method()
			return True
		return False

	def __lt__(self, other):
		if not isinstance(other, UiProjectItem):
			return False
		return self.project < other.project
