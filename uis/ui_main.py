from PyQt5.QtCore import Qt
from PySide2 import QtCore, QtUiTools, QtGui
import utils
from uis.ui_project_bar import UiProjectsBar
from uis.ui_timeline import UiTimeline


class UiMainWindow:
	def __init__(self):
		self.window = QtUiTools.QUiLoader().load("./uis/res/ui_main.ui")

		self.window.toggle_menu_btn.setIcon(QtGui.QIcon(utils.icons_folder + "burger.png"))
		self.window.create_project_btn.setIcon(QtGui.QIcon(utils.icons_folder + "plus.png"))
		self.window.create_project_btn.setIconSize(QtCore.QSize(50, 50))

		self.window.timeline_area.hide()

		self.window.projects_scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.window.projects_scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

		self.window.toggle_menu_btn.clicked.connect(lambda: self.toggle_menu(55, 250))
		self.timeline = UiTimeline(self.window.timeline_area)
		self.projects_bar = UiProjectsBar(self.window.projects_area)

	def toggle_menu(self, min_extend, max_extend):
		width = self.window.sidebar_frame.width()
		width_extend = max_extend if width == min_extend else min_extend

		self.window.animation = QtCore.QPropertyAnimation(self.window.sidebar_frame, b"maximumWidth")
		self.window.animation.setDuration(400)
		self.window.animation.setStartValue(width)
		self.window.animation.setEndValue(width_extend)
		self.window.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
		self.window.animation.start()
