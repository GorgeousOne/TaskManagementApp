import sys
from PySide2.QtWidgets import QApplication, QDialog, QLineEdit, QPlainTextEdit, QDateEdit, QTimeEdit, QHBoxLayout, \
	QCheckBox, QVBoxLayout, QPushButton, QGridLayout, QWidget
from PySide2.QtGui import QFont
from PySide2.QtCore import QCoreApplication, QMetaObject, QDate, QTime, Qt, QSize


class NoteForm(QDialog):
	def __init__(self):
		super().__init__(None)  # , QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint

		segoe_font = QFont("Segoe UI Light", 12)
		self.setFont(segoe_font)

		self.setFixedSize(QSize(350, 420))
		self.verticalLayout = QVBoxLayout(self)
		self.verticalLayout.setContentsMargins(30, 30, 30, 30)
		self.verticalLayout.setSpacing(20)
		self.verticalLayout.setObjectName("verticalLayout")

		self.title = QLineEdit(self)
		self.title.setObjectName("title")
		self.title.setFont(QFont("Segoe UI semibold", 12))
		self.verticalLayout.addWidget(self.title)

		self.description = QPlainTextEdit(self)
		self.description.setObjectName("description")
		self.description.setMaximumHeight(120)
		self.description.setFont(QFont("Segoe UI", 12))
		self.verticalLayout.addWidget(self.description)

		self.grid_widget = QWidget(self)
		self.grid_widget.setObjectName("widget")
		self.verticalLayout.addWidget(self.grid_widget)

		self.gridLayout_2 = QGridLayout(self.grid_widget)
		self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
		self.gridLayout_2.setHorizontalSpacing(20)
		self.gridLayout_2.setObjectName("gridLayout_2")

		self.date_picker = QDateEdit(calendarPopup=True)
		self.date_picker.setObjectName("date_picker")
		self.gridLayout_2.addWidget(self.date_picker, 0, 0, 1, 1)

		self.time_picker = QTimeEdit(self)
		self.time_picker.hide()
		self.time_picker.setObjectName("time_picker")
		self.gridLayout_2.addWidget(self.time_picker, 0, 1, 1, 1)

		self.enable_time = QCheckBox(self)
		self.enable_time.setObjectName("enable_time")
		self.enable_time.setLayoutDirection(Qt.RightToLeft)
		self.verticalLayout.addWidget(self.enable_time)

		self.verticalLayout.addStretch(1)

		self.horizontalLayout_3 = QHBoxLayout()
		self.horizontalLayout_3.setObjectName("horizontalLayout_3")
		self.verticalLayout.addLayout(self.horizontalLayout_3)

		self.btn_cancel = QPushButton(self)
		self.btn_cancel.setObjectName("btn_cancel")
		self.horizontalLayout_3.addWidget(self.btn_cancel)
		self.horizontalLayout_3.addStretch(1)

		self.btn_create = QPushButton(self)
		self.btn_create.setObjectName("btn_create")
		self.btn_create.setEnabled(False)
		self.horizontalLayout_3.addWidget(self.btn_create)

		self.enable_time.stateChanged.connect(self.toggle_time)
		self.title.textChanged.connect(self.toggle_btn_create)
		self.btn_cancel.clicked.connect(self.hide)

		self.retranslate_ui()
		QMetaObject.connectSlotsByName(self)

	def toggle_time(self):
		self.time_picker.setVisible(self.enable_time.isChecked())

	def toggle_btn_create(self, text):
		self.btn_create.setEnabled(len(text.strip()) > 0)

	def show_updated(self):
		"""Reset any previous inputs and update date and time picker before showing"""
		self.title.setText("")
		self.description.setPlainText("")
		self.enable_time.setChecked(False)

		now = QTime.currentTime()
		next_quarter = (now.minute() + 18) // 15 * 15
		time = QTime(now.hour() + next_quarter // 60, next_quarter % 60)

		self.time_picker.setTime(time)
		self.date_picker.setDate(QDate.currentDate())
		self.show()

	def retranslate_ui(self):
		_translate = QCoreApplication.translate
		self.setWindowTitle(_translate("self", "Create new note"))
		self.title.setPlaceholderText(_translate("self", "Add title"))
		self.description.setPlaceholderText(_translate("self", "Add description"))
		self.enable_time.setText(_translate("self", "Add a time"))
		self.btn_cancel.setText(_translate("self", "Cancel"))
		self.btn_create.setText(_translate("self", "Create"))


if __name__ == '__main__':

	app = QApplication(sys.argv)
	window = NoteForm()
	window.show()
	sys.exit(app.exec_())
