
from PySide2 import QtUiTools, QtCore, QtWidgets, QtGui
from PySide2.QtCore import Qt


class UiNoteEditor:
	def __init__(self):
		self.dialog = QtUiTools.QUiLoader().load("./uis/res/ui_note_editor.ui")
		self.dialog.setWindowModality(Qt.ApplicationModal)
		self.dialog.setWindowFlags(Qt.FramelessWindowHint)
		self.dialog.setAttribute(Qt.WA_TranslucentBackground, True)

		shadow = QtWidgets.QGraphicsDropShadowEffect(self.dialog)
		shadow.setBlurRadius(30)
		shadow.setOffset(0)
		shadow.setColor(QtGui.QColor(0, 0, 0, 100))
		self.dialog.frame.setGraphicsEffect(shadow)
		self.dialog.description_edit.setPlaceholderText("Add description")

		self.dialog.date_picker.calendarPopup = True
		self.dialog.time_picker.hide()
		self.dialog.enable_time_check.stateChanged.connect(self.toggle_time_visibility)
		self.dialog.title_edit.textChanged.connect(self.toggle_btn_create)
		self.dialog.cancel_btn.clicked.connect(self.dialog.hide)

	def toggle_time_visibility(self):
		"""show or hide the time picker when checked"""
		self.dialog.time_picker.setVisible(self.dialog.enable_time_check.isChecked())

	def toggle_btn_create(self, text):
		"""enable or disable the create button depending if the title is set"""
		enable = len(text.strip()) > 0
		self.dialog.create_btn.setEnabled(enable)

	def show_updated(self):
		"""Reset any previous inputs and update date and time picker before showing"""
		self.clear()
		now = QtCore.QTime.currentTime()
		next_quarter = (now.minute() + 18) // 15 * 15
		time = QtCore.QTime(now.hour() + next_quarter // 60, next_quarter % 60)

		self.dialog.time_picker.setTime(time)
		self.dialog.date_picker.setDate(QtCore.QDate.currentDate())
		self.dialog.show()
		self.dialog.title_edit.setFocus()

	def clear(self):
		self.dialog.title_edit.setText("")
		self.dialog.description_edit.setPlainText("")
		self.dialog.enable_time_check.setChecked(False)
		self.dialog.create_btn.setEnabled(False)
