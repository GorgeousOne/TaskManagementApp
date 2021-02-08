import sys
from PySide2.QtWidgets import QApplication, QDialog, QLineEdit, QPlainTextEdit, QDateEdit, QTimeEdit, QHBoxLayout, \
	QCheckBox, QVBoxLayout, QPushButton, QSpacerItem, QSizePolicy
from PySide2.QtGui import QFont
from PySide2.QtCore import QCoreApplication, QMetaObject, QDate, QTime


class NoteForm2(QDialog):
	def __init__(self):
		super().__init__(None)  # , QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint

		self.resize(400, 300)
		self.verticalLayout = QVBoxLayout(self)
		self.verticalLayout.setContentsMargins(30, 30, 30, 30)
		self.verticalLayout.setSpacing(6)
		self.verticalLayout.setObjectName("verticalLayout")

		self.title = QLineEdit(self)
		self.title.setObjectName("title")
		self.verticalLayout.addWidget(self.title)

		self.description = QPlainTextEdit(self)
		self.description.setObjectName("description")
		self.verticalLayout.addWidget(self.description)

		self.date_picker = QDateEdit(calendarPopup=True)
		self.date_picker.setObjectName("date_picker")
		self.date_picker.setDate(QDate.currentDate())
		self.verticalLayout.addWidget(self.date_picker)

		self.horizontalLayout_2 = QHBoxLayout()
		self.horizontalLayout_2.setObjectName("horizontalLayout_2")
		self.verticalLayout.addLayout(self.horizontalLayout_2)

		self.enable_time = QCheckBox(self)
		self.enable_time.setObjectName("enable_time")
		self.horizontalLayout_2.addWidget(self.enable_time)

		self.time_picker = QTimeEdit(self)
		self.time_picker.setEnabled(False)
		self.time_picker.setObjectName("time_picker")
		now = QTime.currentTime()
		next_quarter = (now.minute() // 15 + 1) * 15
		time = QTime(now.hour() + next_quarter // 60, next_quarter % 60)
		self.time_picker.setTime(time)

		self.horizontalLayout_2.addWidget(self.time_picker)

		self.horizontalLayout_3 = QHBoxLayout()
		self.horizontalLayout_3.setObjectName("horizontalLayout_3")
		self.verticalLayout.addLayout(self.horizontalLayout_3)

		self.btn_cancel = QPushButton(self)
		self.btn_cancel.setObjectName("btn_cancel")
		self.horizontalLayout_3.addWidget(self.btn_cancel)

		spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
		self.horizontalLayout_3.addItem(spacerItem)

		self.btn_create = QPushButton(self)
		self.btn_create.setObjectName("btn_create")
		self.btn_create.setEnabled(False)
		self.horizontalLayout_3.addWidget(self.btn_create)

		self.enable_time.stateChanged.connect(self.toggle_time)
		self.title.textChanged.connect(self.toggle_btn_create)

		self.retranslate_ui()
		QMetaObject.connectSlotsByName(self)

	def toggle_time(self):
		self.time_picker.setEnabled(self.enable_time.isChecked())

	def toggle_btn_create(self, text):
		self.btn_create.setEnabled(len(text) > 0)

	def retranslate_ui(self):
		_translate = QCoreApplication.translate
		self.setWindowTitle(_translate("self", "Create new note"))
		self.title.setPlaceholderText(_translate("self", "Add title"))
		self.description.setPlaceholderText(_translate("self", "Add description"))
		self.enable_time.setText(_translate("self", "Add a time"))
		self.btn_cancel.setText(_translate("self", "Cancel"))
		self.btn_create.setText(_translate("self", "Create"))


if __name__ == '__main__':
	segoe_font = QFont("Segoe UI Light", 10)

	app = QApplication(sys.argv)
	app.setFont(segoe_font)

	window = NoteForm2()
	window.show()
	sys.exit(app.exec_())
