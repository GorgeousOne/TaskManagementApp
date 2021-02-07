# WARNING! All changes made in this file will be lost when recompiling UI file!

from PySide2.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
                            QRect, QSize, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
                           QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
                           QRadialGradient)
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
	def setupUi(self, MainWindow):
		if MainWindow.objectName():
			MainWindow.setObjectName(u"MainWindow")
		MainWindow.resize(900, 550)
		MainWindow.setMinimumSize(QSize(900, 550))
		MainWindow.setStyleSheet(u"background-color: rgb(243, 243, 243);")

		self.centralwidget = QWidget(MainWindow)
		self.centralwidget.setObjectName(u"centralwidget")
		MainWindow.setCentralWidget(self.centralwidget)

		self.verticalLayout = QVBoxLayout(self.centralwidget)
		self.verticalLayout.setSpacing(0)
		self.verticalLayout.setObjectName(u"verticalLayout")
		self.verticalLayout.setContentsMargins(0, 0, 0, 0)

		self.top_bar = QFrame(self.centralwidget)
		self.top_bar.setObjectName(u"Top_Bar")
		self.top_bar.setMaximumSize(QSize(16777215, 40))
		self.top_bar.setStyleSheet(u"background-color: rgb(255, 255, 255);")
		self.top_bar.setFrameShape(QFrame.NoFrame)
		self.top_bar.setFrameShadow(QFrame.Raised)
		self.verticalLayout.addWidget(self.top_bar)

		self.horizontalLayout = QHBoxLayout(self.top_bar)
		self.horizontalLayout.setSpacing(0)
		self.horizontalLayout.setObjectName(u"horizontalLayout")
		self.horizontalLayout.setContentsMargins(0, 0, 0, 0)

		self.frame_toggle = QFrame(self.top_bar)
		self.frame_toggle.setObjectName(u"frame_toggle")
		self.frame_toggle.setMaximumSize(QSize(70, 40))
		self.frame_toggle.setStyleSheet(u"background-color: rgb(66, 135, 245);")
		self.frame_toggle.setFrameShape(QFrame.StyledPanel)
		self.frame_toggle.setFrameShadow(QFrame.Raised)
		self.horizontalLayout.addWidget(self.frame_toggle)

		self.verticalLayout_2 = QVBoxLayout(self.frame_toggle)
		self.verticalLayout_2.setSpacing(0)
		self.verticalLayout_2.setObjectName(u"verticalLayout_2")
		self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)

		self.btn_toggle = QPushButton(self.frame_toggle)
		self.btn_toggle.setObjectName(u"btn_toggle")

		sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.btn_toggle.sizePolicy().hasHeightForWidth())

		self.btn_toggle.setSizePolicy(sizePolicy)
		self.btn_toggle.setStyleSheet(u"color: rgb(255, 255, 255);\nborder: 0px solid;")
		self.verticalLayout_2.addWidget(self.btn_toggle)

		self.frame_top = QFrame(self.top_bar)
		self.frame_top.setObjectName(u"frame_top")
		self.frame_top.setFrameShape(QFrame.StyledPanel)
		self.frame_top.setFrameShadow(QFrame.Raised)
		self.horizontalLayout.addWidget(self.frame_top)

		self.Content = QFrame(self.centralwidget)
		self.Content.setObjectName(u"Content")
		self.Content.setFrameShape(QFrame.NoFrame)
		self.Content.setFrameShadow(QFrame.Raised)
		self.verticalLayout.addWidget(self.Content)

		self.horizontal_layout_2 = QHBoxLayout(self.Content)
		self.horizontal_layout_2.setSpacing(0)
		self.horizontal_layout_2.setObjectName(u"horizontalLayout_2")
		self.horizontal_layout_2.setContentsMargins(0, 0, 0, 0)

		self.frame_left_menu = QFrame(self.Content)
		self.frame_left_menu.setObjectName(u"frame_left_menu")
		self.frame_left_menu.setMinimumSize(QSize(70, 0))
		self.frame_left_menu.setMaximumSize(QSize(70, 16777215))
		self.frame_left_menu.setStyleSheet(u"background-color: rgb(0, 102, 255);")
		self.frame_left_menu.setFrameShape(QFrame.StyledPanel)
		self.frame_left_menu.setFrameShadow(QFrame.Raised)
		self.horizontal_layout_2.addWidget(self.frame_left_menu)

		self.verticalLayout_3 = QVBoxLayout(self.frame_left_menu)
		self.verticalLayout_3.setObjectName(u"verticalLayout_3")
		self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)

		self.frame_top_menus = QFrame(self.frame_left_menu)
		self.frame_top_menus.setObjectName(u"frame_top_menus")
		self.frame_top_menus.setFrameShape(QFrame.NoFrame)
		self.frame_top_menus.setFrameShadow(QFrame.Raised)
		self.frame_top_menus.setStyleSheet(
			u".QPushButton {\n"
			"	color: rgb(255, 255, 255);\n"
			"	background-color: rgb(35, 35, 35);\n"
			"	border: 0px solid;\n"
			"}\n"
			".QPushButton:hover {\n"
			"	background-color: rgb(85, 170, 255);\n"
			"}")
		self.verticalLayout_3.addWidget(self.frame_top_menus, 0, Qt.AlignTop)

		self.verticalLayout_4 = QVBoxLayout(self.frame_top_menus)
		self.verticalLayout_4.setSpacing(0)
		self.verticalLayout_4.setObjectName(u"verticalLayout_4")
		self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)

		self.btn_page_1 = QPushButton(self.frame_top_menus)
		self.btn_page_1.setObjectName(u"btn_page_1")
		self.btn_page_1.setMinimumSize(QSize(0, 40))
		self.verticalLayout_4.addWidget(self.btn_page_1)

		self.btn_page_2 = QPushButton(self.frame_top_menus)
		self.btn_page_2.setObjectName(u"btn_page_2")
		self.btn_page_2.setMinimumSize(QSize(0, 40))
		self.verticalLayout_4.addWidget(self.btn_page_2)

		self.btn_page_3 = QPushButton(self.frame_top_menus)
		self.btn_page_3.setObjectName(u"btn_page_3")
		self.btn_page_3.setMinimumSize(QSize(0, 40))
		self.verticalLayout_4.addWidget(self.btn_page_3)

		self.frame_pages = QFrame(self.Content)
		self.frame_pages.setObjectName(u"frame_pages")
		self.frame_pages.setFrameShape(QFrame.StyledPanel)
		self.frame_pages.setFrameShadow(QFrame.Raised)
		self.horizontal_layout_2.addWidget(self.frame_pages)

		self.verticalLayout_5 = QVBoxLayout(self.frame_pages)
		self.verticalLayout_5.setObjectName(u"verticalLayout_5")

		self.stackedWidget = QStackedWidget(self.frame_pages)
		self.stackedWidget.setObjectName(u"stackedWidget")
		self.stackedWidget.setCurrentIndex(0)
		self.verticalLayout_5.addWidget(self.stackedWidget)

		self.page_1 = QWidget()
		self.page_1.setObjectName(u"page_1")
		self.stackedWidget.addWidget(self.page_1)

		self.verticalLayout_7 = QVBoxLayout(self.page_1)
		self.verticalLayout_7.setObjectName(u"verticalLayout_7")
		self.verticalLayout_7.setAlignment(Qt.AlignTop)
		# self.label_1 = QLabel(self.page_1)
		# self.label_1.setObjectName(u"label_1")
		# self.label_1.setAlignment(Qt.AlignCenter)
		# self.verticalLayout_7.addWidget(self.label_1)

		self.page_2 = QWidget()
		self.page_2.setObjectName(u"page_2")
		self.stackedWidget.addWidget(self.page_2)

		self.verticalLayout_6 = QVBoxLayout(self.page_2)
		self.verticalLayout_6.setObjectName(u"verticalLayout_6")

		self.label_2 = QLabel(self.page_2)
		self.label_2.setObjectName(u"label_2")
		self.label_2.setAlignment(Qt.AlignCenter)
		self.verticalLayout_6.addWidget(self.label_2)

		self.page_3 = QWidget()
		self.page_3.setObjectName(u"page_3")
		self.stackedWidget.addWidget(self.page_3)

		self.vertical_layout_8 = QVBoxLayout(self.page_3)
		self.vertical_layout_8.setObjectName(u"vertical_layout_8")

		self.label_3 = QLabel(self.page_3)
		self.label_3.setObjectName(u"label_3")
		self.label_3.setAlignment(Qt.AlignCenter)
		self.vertical_layout_8.addWidget(self.label_3)

		self.retranslateUi(MainWindow)
		QMetaObject.connectSlotsByName(MainWindow)

	def retranslateUi(self, MainWindow):
		MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
		self.btn_toggle.setText(QCoreApplication.translate("MainWindow", u"TOGGLE", None))
		self.btn_page_1.setText(QCoreApplication.translate("MainWindow", u"Page 1", None))
		self.btn_page_2.setText(QCoreApplication.translate("MainWindow", u"Page 2", None))
		self.btn_page_3.setText(QCoreApplication.translate("MainWindow", u"Page 3", None))
		# self.label_1.setText(QCoreApplication.translate("MainWindow", u"PAGE 1", None))
		self.label_2.setText(QCoreApplication.translate("MainWindow", u"PAGE 2", None))
		self.label_3.setText(QCoreApplication.translate("MainWindow", u"PAGE 3", None))
