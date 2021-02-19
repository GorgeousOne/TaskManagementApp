from PySide2 import QtCore
from PySide2 import QtUiTools
from PySide2 import QtGui

from utils import icons_folder

from uis.ui_timeline import UITimeline


class UIMainWindow:
	def __init__(self):
		self.window = QtUiTools.QUiLoader().load("./uis/res/ui_main.ui")

		self.window.toggle_menu_btn.setIcon(QtGui.QIcon(icons_folder + "burger.png"))
		self.window.timeline_area.hide()
		self.timeline = UITimeline(self.window.timeline_area)

		self.window.toggle_menu_btn.clicked.connect(lambda: self.toggle_menu(60, 150))
		self.window.page1_btn.clicked.connect(lambda: self.window.page_stack.setCurrentWidget(self.window.page1_widget))
		self.window.page2_btn.clicked.connect(lambda: self.window.page_stack.setCurrentWidget(self.window.page2_widget))

	def toggle_menu(self, min_extend, max_extend):
		width = self.window.sidebar_frame.width()
		width_extend = max_extend if width == min_extend else min_extend

		self.window.animation = QtCore.QPropertyAnimation(self.window.sidebar_frame, b"minimumWidth")
		self.window.animation.setDuration(400)
		self.window.animation.setStartValue(width)
		self.window.animation.setEndValue(width_extend)
		self.window.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
		self.window.animation.start()
