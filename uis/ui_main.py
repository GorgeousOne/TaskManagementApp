from PySide2 import QtCore
from PySide2.QtCore import QPropertyAnimation
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QIcon

from utils import icons_folder


class UIMainWindow:
	def __init__(self):
		self.window = QUiLoader().load("./uis/res/ui_main.ui")

		self.window.toggle_menu_btn.setIcon(QIcon(icons_folder + "burger.png"))
		self.window.create_note_btn.setIcon(QIcon(icons_folder + "plus.png"))

		self.window.toggle_menu_btn.clicked.connect(lambda: self.toggle_menu(50, 250))
		self.window.page1_btn.clicked.connect(lambda: self.window.page_stack.setCurrentWidget(self.window.page1_widget))
		self.window.page2_btn.clicked.connect(lambda: self.window.page_stack.setCurrentWidget(self.window.page2_widget))
		self.window.page3_btn.clicked.connect(lambda: self.window.page_stack.setCurrentWidget(self.window.page3_widget))

	def toggle_menu(self, min_extend, max_extend):
		width = self.window.sidebar_frame.width()
		width_extend = max_extend if width == min_extend else min_extend

		self.window.animation = QPropertyAnimation(self.window.sidebar_frame, b"minimumWidth")
		self.window.animation.setDuration(400)
		self.window.animation.setStartValue(width)
		self.window.animation.setEndValue(width_extend)
		self.window.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
		self.window.animation.start()
