from PySide2 import QtWidgets, QtUiTools

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
		self.project_change_event(self.project)

	def enterEvent(self, event):
		self.content.button_bar.show()

	def leaveEvent(self, event):
		self.content.button_bar.hide()

	def project_change_event(self, project):
		project_name = self.project.get_name()
		self.content.name_label.setText(project_name)
		self.content.icon_label.setText(project_name[0].upper())
		icon_style = utils.replace_property(self.content.icon_label.styleSheet(), "background", self.project.get_color().name())
		self.content.icon_label.setStyleSheet(icon_style)

	def __lt__(self, other):
		if not isinstance(other, UiProjectItem):
			return False
		return self.project < other.project
