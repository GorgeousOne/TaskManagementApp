from PySide2.QtCore import QCoreApplication, QMetaObject, QSize, Qt, QFile
from PySide2.QtWidgets import *
from PySide2.QtGui import QIcon
import os
from os.path import sep


class Ui_MainWindow(object):
	def setup_ui(self, main_window):
		if main_window.objectName():
			main_window.setObjectName("MainWindow")
		main_window.resize(900, 550)
		main_window.setMinimumSize(QSize(900, 550))
		main_window.setStyleSheet("background-color: rgb(45, 45, 45);")

		self.centralwidget = QWidget(main_window)
		self.centralwidget.setObjectName("centralwidget")
		main_window.setCentralWidget(self.centralwidget)

		self.verticalLayout = QVBoxLayout(self.centralwidget)
		self.verticalLayout.setSpacing(0)
		self.verticalLayout.setObjectName("verticalLayout")
		self.verticalLayout.setContentsMargins(0, 0, 0, 0)

		self.top_bar = QFrame(self.centralwidget)
		self.top_bar.setObjectName("Top_Bar")
		self.top_bar.setMaximumSize(QSize(16777215, 50))
		self.top_bar.setStyleSheet("background-color: rgb(55, 55, 55);")
		self.top_bar.setFrameShape(QFrame.NoFrame)
		self.top_bar.setFrameShadow(QFrame.Raised)
		self.verticalLayout.addWidget(self.top_bar)

		self.horizontalLayout = QHBoxLayout(self.top_bar)
		self.horizontalLayout.setSpacing(0)
		self.horizontalLayout.setObjectName("horizontalLayout")
		self.horizontalLayout.setContentsMargins(0, 0, 0, 0)

		self.frame_toggle = QFrame(self.top_bar)
		self.frame_toggle.setObjectName("frame_toggle")
		self.frame_toggle.setMaximumSize(QSize(50, 16777215))
		self.frame_toggle.setStyleSheet("background-color: rgb(35, 35, 35);")
		self.frame_toggle.setFrameShape(QFrame.StyledPanel)
		self.frame_toggle.setFrameShadow(QFrame.Raised)
		self.horizontalLayout.addWidget(self.frame_toggle)

		self.verticalLayout_2 = QVBoxLayout(self.frame_toggle)
		self.verticalLayout_2.setSpacing(0)
		self.verticalLayout_2.setObjectName("verticalLayout_2")
		self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)

		self.btn_toggle_menu = QPushButton(self.frame_toggle)
		self.btn_toggle_menu.setObjectName("btn_toggle")

		sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)

		self.btn_toggle_menu.setSizePolicy(sizePolicy)
		self.btn_toggle_menu.setStyleSheet("color: rgb(255, 255, 255);\nborder: none;")
		self.verticalLayout_2.addWidget(self.btn_toggle_menu)

		self.frame_top = QFrame(self.top_bar)
		self.frame_top.setObjectName("frame_top")
		self.frame_top.setFrameShape(QFrame.StyledPanel)
		self.frame_top.setFrameShadow(QFrame.Raised)
		self.horizontalLayout.addWidget(self.frame_top)

		self.frame_top.setStyleSheet(
			".QPushButton {\n"
			"	color: rgb(255, 255, 255);\n"
			"	background-color: rgb(75, 75, 75);\n"
			"	border: none;\n"
			"}\n"
			".QPushButton:hover:!pressed {\n"
			"   background-color: rgb(95, 95, 95);\n"
			"}")

		self.horizontal_layout_3 = QHBoxLayout(self.frame_top)
		self.horizontal_layout_3.setSpacing(0)
		self.horizontal_layout_3.setObjectName("horizontalLayout")
		self.horizontal_layout_3.setContentsMargins(0, 0, 0, 0)

		self.btn_add_note = QPushButton(self.frame_top)
		self.btn_add_note.setObjectName("btn_add_note")
		self.btn_add_note.setMinimumSize(QSize(50, 50))

		root_dir = os.path.dirname(os.path.abspath("main.py"))
		self.btn_add_note.setIcon(QIcon(root_dir + sep + "uis" + sep + "icons" + sep + "plus.png"))
		self.btn_add_note.setIconSize(QSize(50, 50))
		self.horizontal_layout_3.addWidget(self.btn_add_note)

		self.horizontal_layout_3.addStretch(1)

		self.content = QFrame(self.centralwidget)
		self.content.setObjectName("content")
		self.content.setFrameShape(QFrame.NoFrame)
		self.content.setFrameShadow(QFrame.Raised)
		self.verticalLayout.addWidget(self.content)

		self.horizontal_layout_2 = QHBoxLayout(self.content)
		self.horizontal_layout_2.setSpacing(0)
		self.horizontal_layout_2.setObjectName("horizontalLayout_2")
		self.horizontal_layout_2.setContentsMargins(0, 0, 0, 0)

		self.frame_left_menu = QFrame(self.content)
		self.frame_left_menu.setObjectName("frame_left_men")
		self.frame_left_menu.setMinimumSize(QSize(50, 0))
		self.frame_left_menu.setMaximumSize(QSize(50, 16777215))
		self.frame_left_menu.setStyleSheet("background-color: rgb(35, 35, 35);")
		self.frame_left_menu.setFrameShape(QFrame.StyledPanel)
		self.frame_left_menu.setFrameShadow(QFrame.Raised)
		self.horizontal_layout_2.addWidget(self.frame_left_menu)

		self.verticalLayout_3 = QVBoxLayout(self.frame_left_menu)
		self.verticalLayout_3.setObjectName("verticalLayout_3")
		self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)

		self.frame_top_menus = QFrame(self.frame_left_menu)
		self.frame_top_menus.setObjectName("frame_top_menus")
		self.frame_top_menus.setFrameShape(QFrame.NoFrame)
		self.frame_top_menus.setFrameShadow(QFrame.Raised)
		self.frame_top_menus.setStyleSheet(
			".QPushButton {\n"
			"	color: rgb(255, 255, 255);\n"
			"	background-color: rgb(35, 35, 35);\n"
			"	border: none;\n"
			"}\n"
			".QPushButton:hover:!pressed {\n"
			"	background-color: rgb(55, 55, 55);\n"
			"}")
		self.verticalLayout_3.addWidget(self.frame_top_menus, 0, Qt.AlignTop)

		self.verticalLayout_4 = QVBoxLayout(self.frame_top_menus)
		self.verticalLayout_4.setSpacing(0)
		self.verticalLayout_4.setObjectName("verticalLayout_4")
		self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)

		self.btn_page_1 = QPushButton(self.frame_top_menus)
		self.btn_page_1.setObjectName("btn_page_1")
		self.btn_page_1.setMinimumSize(QSize(0, 50))
		self.verticalLayout_4.addWidget(self.btn_page_1)

		self.btn_page_2 = QPushButton(self.frame_top_menus)
		self.btn_page_2.setObjectName("btn_page_2")
		self.btn_page_2.setMinimumSize(QSize(0, 50))
		self.verticalLayout_4.addWidget(self.btn_page_2)

		self.btn_page_3 = QPushButton(self.frame_top_menus)
		self.btn_page_3.setObjectName("btn_page_3")
		self.btn_page_3.setMinimumSize(QSize(0, 50))
		self.verticalLayout_4.addWidget(self.btn_page_3)

		self.frame_pages = QFrame(self.content)
		self.frame_pages.setObjectName("frame_pages")
		self.frame_pages.setFrameShape(QFrame.StyledPanel)
		self.frame_pages.setFrameShadow(QFrame.Raised)
		self.horizontal_layout_2.addWidget(self.frame_pages)

		self.verticalLayout_5 = QVBoxLayout(self.frame_pages)
		self.verticalLayout_5.setObjectName("verticalLayout_5")

		self.stackedWidget = QStackedWidget(self.frame_pages)
		self.stackedWidget.setObjectName("stackedWidget")
		self.stackedWidget.setCurrentIndex(0)
		self.verticalLayout_5.addWidget(self.stackedWidget)

		self.page_1 = QWidget()
		self.page_1.setObjectName("page_1")
		self.stackedWidget.addWidget(self.page_1)

		self.verticalLayout_7 = QVBoxLayout(self.page_1)
		self.verticalLayout_7.setObjectName("verticalLayout_7")
		self.verticalLayout_7.setAlignment(Qt.AlignTop)

		self.page_2 = QWidget()
		self.page_2.setObjectName("page_2")
		self.stackedWidget.addWidget(self.page_2)

		self.verticalLayout_6 = QVBoxLayout(self.page_2)
		self.verticalLayout_6.setObjectName("verticalLayout_6")

		self.label_2 = QLabel(self.page_2)
		self.label_2.setObjectName("label_2")
		self.label_2.setAlignment(Qt.AlignCenter)
		self.verticalLayout_6.addWidget(self.label_2)

		self.page_3 = QWidget()
		self.page_3.setObjectName("page_3")
		self.stackedWidget.addWidget(self.page_3)

		self.vertical_layout_8 = QVBoxLayout(self.page_3)
		self.vertical_layout_8.setObjectName("vertical_layout_8")

		self.label_3 = QLabel(self.page_3)
		self.label_3.setObjectName("label_3")
		self.label_3.setAlignment(Qt.AlignCenter)
		self.vertical_layout_8.addWidget(self.label_3)

		self.retranslateUi(main_window)
		QMetaObject.connectSlotsByName(main_window)

	def retranslateUi(self, MainWindow):
		MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", "MainWindow", None))
		self.btn_toggle_menu.setText(QCoreApplication.translate("MainWindow", "TOGGLE", None))
		self.btn_page_1.setText(QCoreApplication.translate("MainWindow", "Page 1", None))
		self.btn_page_2.setText(QCoreApplication.translate("MainWindow", "Page 2", None))
		self.btn_page_3.setText(QCoreApplication.translate("MainWindow", "Page 3", None))
		self.label_2.setText(QCoreApplication.translate("MainWindow", "PAGE 2", None))
		self.label_3.setText(QCoreApplication.translate("MainWindow", "PAGE 3", None))
