from PySide2 import QtWidgets, QtUiTools


class UiProjectItem(QtWidgets.QWidget):
	def __init__(self, project, project_bar):
		super().__init__()
		self.project = project
		self.project_bar = project_bar

		self.verticalLayout = QtWidgets.QVBoxLayout(self)
		self.verticalLayout.setContentsMargins(0, 0, 0, 0)
		self.setFixedHeight(40)

		self.content = QtUiTools.QUiLoader().load("./uis/res/ui_project_item.ui")
		self.verticalLayout.addWidget(self.content)

		# self.gray_out_effect = QtWidgets.QGraphicsColorizeEffect(self)
		# self.gray_out_effect.setColor(Qt.black)
		# self.gray_out_effect.setStrength(0.95)
		# self.content.button_layout.setGraphicsEffect(self.gray_out_effect)

		self.update_data()

	def enterEvent(self, event):
		# self.gray_out_effect.setEnabled(False)
		self.content.button_layout.show()

	def leaveEvent(self, event):
		# self.gray_out_effect.setEnabled(True)
		self.content.button_layout.hide()

	def update_data(self):
		project_name = self.project.get_name()
		self.content.name_label.setTexst(project_name)
		self.content.icon_label(project_name[0].upper())
