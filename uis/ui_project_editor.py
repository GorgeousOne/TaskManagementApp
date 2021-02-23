from PySide2 import QtWidgets, QtGui, QtUiTools
from PySide2.QtCore import Qt


class UiProjectEditor:
	def __init__(self):
		self.dialog = QtUiTools.QUiLoader().load("./uis/res/ui_project_editor.ui")
		self.dialog.setWindowModality(Qt.ApplicationModal)
		self.dialog.setWindowFlags(Qt.FramelessWindowHint)
		self.dialog.setAttribute(Qt.WA_TranslucentBackground, True)

		shadow = QtWidgets.QGraphicsDropShadowEffect(self.dialog)
		shadow.setBlurRadius(30)
		shadow.setOffset(0)
		shadow.setColor(QtGui.QColor(0, 0, 0, 100))
		self.dialog.frame.setGraphicsEffect(shadow)

		self.finest_color_selection = [
			QtGui.QColor(214, 0, 0),
			QtGui.QColor(244, 81, 30),
			QtGui.QColor(255, 195, 18),
			QtGui.QColor(163, 203, 56),
			QtGui.QColor(0, 148, 50),
			QtGui.QColor(18, 203, 196),
			QtGui.QColor(63, 81, 181),
			QtGui.QColor(137, 131, 227),
			QtGui.QColor(142, 36, 170),
			QtGui.QColor(181, 52, 113),
			QtGui.QColor(230, 124, 115)
		]

		model = self.dialog.color_combo.model()

		for color in self.finest_color_selection:
			color_item = QtGui.QStandardItem("⬤")
			color_item.setForeground(color)
			color_item.setTextAlignment(Qt.AlignHCenter)
			model.appendRow(color_item)

		self.setup_ui_functions()

	def setup_ui_functions(self):
		self.dialog.name_edit.textChanged.connect(self.toggle_btn_create)
		self.dialog.cancel_btn.clicked.connect(self.dialog.hide)

		self.dialog.color_combo.currentIndexChanged.connect(self.change_combo_color)

	def toggle_btn_create(self, text):
		"""enable or disable the create button depending if the title is set"""
		enable = len(text.strip()) > 0
		self.dialog.create_btn.setEnabled(enable)

	def get_project_name(self):
		return self.dialog.name_edit.text().strip()

	def get_selected_color(self):
		return self.finest_color_selection[self.dialog.color_combo.currentIndex()]

	def set_project_name(self, name):
		return self.dialog.name_edit.setText(name)

	def set_selected_color(self, color):
		index = self.finest_color_selection.index(color)
		if index == -1:
			index = 6
		self.dialog.color_combo.setCurrentIndex(index)

	def show_reset(self):
		self.reset()
		self.dialog.show()

	def reset(self):
		self.set_project_name("")
		self.set_selected_color(self.finest_color_selection[6])

	def change_combo_color(self, index=6):
		self.dialog.color_combo.setStyleSheet("color: " + self.finest_color_selection[index].name())
