
from PySide2.QtCore import QDate, QTime, Qt
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QGraphicsDropShadowEffect
from PySide2.QtGui import QColor


class UIProjectEditor:
	def __init__(self):
		self.dialog = QUiLoader().load("./uis/res/ui_project_editor.ui")
		self.dialog.setWindowModality(Qt.ApplicationModal)
		self.dialog.setWindowFlags(Qt.FramelessWindowHint)
		self.dialog.setAttribute(Qt.WA_TranslucentBackground, True)

		shadow = QGraphicsDropShadowEffect(self.dialog)
		shadow.setBlurRadius(30)
		shadow.setOffset(0)
		shadow.setColor(QColor(0, 0, 0, 100))
		self.dialog.frame.setGraphicsEffect(shadow)
		self.dialog.name_edit.textChanged.connect(self.toggle_btn_create)
		self.dialog.cancel_btn.clicked.connect(self.dialog.hide)
		
	def toggle_btn_create(self, text):
		"""enable or disable the create button depending if the title is set"""
		enable = len(text.strip()) > 0
		self.dialog.create_btn.setEnabled(enable)
