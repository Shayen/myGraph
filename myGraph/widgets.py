import sys

from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

class Console(QPlainTextEdit):

	def __init__(self, parent=None):
		super(Console, self).__init__(parent)

		self.setWordWrapMode(QTextOption.NoWrap)
		self.setStyleSheet("""
		QPlainTextEdit{
			color: white;
			background-color: black;
			border: none;
		}
		""")
		self.setReadOnly(True)
		self.setTextInteractionFlags(Qt.TextSelectableByMouse)

		startupText = "Start console...\n\n"

		self.append(startupText)

	def contextMenuEvent(self, event):
		menu = self.createStandardContextMenu()
		action = menu.addAction(self.tr("Clear"))
		action.triggered.connect(self.clear)
		menu.exec_(QCursor.pos())

	def append(self, message, isError=False):

		color = 'white'
		try:
			if isError:
				color = 'red'
				sys.__stderr__.write(message)
			else:
				sys.__stdout__.write(message)
		except Exception as e:
			message += '</font>\n\n<font color=\"orange\"> [Warning] Cannot stream I/O to main PIPE : ' + str(e)

		message = message.replace("\n", "<br>")
		message = message.replace(" ", "&nbsp;&nbsp;")

		cursor = self.textCursor()
		cursor.movePosition(QTextCursor.End)
		cursor.insertHtml("<font color=\"%s\">" % color + message + "</font>")
		self.setTextCursor(cursor)
		self.ensureCursorVisible()