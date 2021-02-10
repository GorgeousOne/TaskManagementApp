
from PySide2.QtCore import QDate, QTime, Qt
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QGraphicsDropShadowEffect


class UINoteEditor:
	def __init__(self):

		self.dialog = QUiLoader().load("./uis/res/ui_note_editor.ui")
		self.dialog.setWindowModality(Qt.ApplicationModal)
		self.dialog.setWindowFlags(Qt.FramelessWindowHint)
		self.dialog.setAttribute(Qt.WA_TranslucentBackground, True)

		shadow = QGraphicsDropShadowEffect(self.dialog)
		shadow.setBlurRadius(20)
		shadow.setOffset(0)
		shadow.setColor(Qt.black)
		self.dialog.frame.setGraphicsEffect(shadow)
		self.dialog.description_edit.setPlaceholderText("Add description")

		self.dialog.time_picker.hide()
		self.dialog.enable_time_check.stateChanged.connect(self.toggle_time_visibility)
		self.dialog.title_edit.textChanged.connect(self.toggle_btn_create)
		self.dialog.cancel_btn.clicked.connect(self.dialog.hide)

	def toggle_time_visibility(self):
		"""show or hide the time picker when needed"""
		self.dialog.time_picker.setVisible(self.dialog.enable_time_check.isChecked())

	def toggle_btn_create(self, text):
		"""enable or disable the create button depending on if the title is set"""
		self.dialog.create_btn.setEnabled(len(text.strip()) > 0)

	def show_updated(self):
		"""Reset any previous inputs and update date and time picker before showing"""
		self.dialog.title_edit.setText("")
		self.dialog.description_edit.setPlainText("")
		self.dialog.enable_time_check.setChecked(False)

		now = QTime.currentTime()
		next_quarter = (now.minute() + 18) // 15 * 15
		time = QTime(now.hour() + next_quarter // 60, next_quarter % 60)

		self.dialog.time_picker.setTime(time)
		self.dialog.date_picker.setDate(QDate.currentDate())
		self.dialog.show()
		self.dialog.setFocus(Qt.PopupFocusReason)