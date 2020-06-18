from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
# from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtPrintSupport import *
import sys
import sqlite3
import time
import os
import requests, json


class StartSensor(QDialog):
	def __init__(self, *args, **kwargs):
		super(StartSensor, self).__init__(*args, **kwargs)

		self.QBtn = QPushButton()
		self.QBtn.setText("Start")

		self.setWindowTitle("Start Sensor")
		self.setFixedWidth(300)
		self.setFixedHeight(100)
		self.QBtn.clicked.connect(self.startsensor)
		layout = QVBoxLayout()

		self.listsensor = QComboBox()

		url = requests.get("http://192.168.56.106:5555/containers/json?all=true")
		json1 = json.loads(url.content)

		for sensor in json1:
			for name in sensor['Names']:
				self.listsensor.addItem(name)

		
		layout.addWidget(self.listsensor)

		layout.addWidget(self.QBtn)
		self.setLayout(layout)

	def startsensor(self):

		sensorpilih = ""
		sensorpilih = self.listsensor.itemText(self.listsensor.currentIndex())
		alamat = "http://192.168.56.106:5555/containers" + sensorpilih + "/start"

		try:
			urlstart = requests.post(alamat)
			QMessageBox.information(QMessageBox(),'Successful','Successful')
			self.close()
		except Exception:
			QMessageBox.warning(QMessageBox(), 'Error', 'Error')

class StopSensor(QDialog):
	def __init__(self, *args, **kwargs):
		super(StopSensor, self).__init__(*args, **kwargs)

		self.QBtn = QPushButton()
		self.QBtn.setText("Stop")

		self.setWindowTitle("Stop Sensor")
		self.setFixedWidth(300)
		self.setFixedHeight(100)
		self.QBtn.clicked.connect(self.stopsensor)
		layout = QVBoxLayout()

		self.listsensor = QComboBox()

		url = requests.get("http://192.168.56.106:5555/containers/json")
		json1 = json.loads(url.content)

		for sensor in json1:
			for name in sensor['Names']:
				self.listsensor.addItem(name)

		
		layout.addWidget(self.listsensor)

		layout.addWidget(self.QBtn)
		self.setLayout(layout)

	def stopsensor(self):

		sensorpilih = ""
		sensorpilih = self.listsensor.itemText(self.listsensor.currentIndex())
		alamat = "http://192.168.56.106:5555/containers" + sensorpilih + "/stop"

		try:
			urlstart = requests.post(alamat)
			QMessageBox.information(QMessageBox(),'Successful','Successful')
			self.close()
		except Exception:
			QMessageBox.warning(QMessageBox(), 'Error', 'Error')

class RestartSensor(QDialog):
	def __init__(self, *args, **kwargs):
		super(RestartSensor, self).__init__(*args, **kwargs)

		self.QBtn = QPushButton()
		self.QBtn.setText("Restart")

		self.setWindowTitle("Restart Sensor")
		self.setFixedWidth(300)
		self.setFixedHeight(100)
		self.QBtn.clicked.connect(self.restartsensor)
		layout = QVBoxLayout()

		self.listsensor = QComboBox()

		url = requests.get("http://192.168.56.106:5555/containers/json")
		json1 = json.loads(url.content)

		for sensor in json1:
			for name in sensor['Names']:
				self.listsensor.addItem(name)

		
		layout.addWidget(self.listsensor)

		layout.addWidget(self.QBtn)
		self.setLayout(layout)

	def restartsensor(self):

		sensorpilih = ""
		sensorpilih = self.listsensor.itemText(self.listsensor.currentIndex())
		alamat = "http://192.168.56.106:5555/containers" + sensorpilih + "/restart"

		try:
			urlstart = requests.post(alamat)
			QMessageBox.information(QMessageBox(),'Successful','Successful')
			self.close()
		except Exception:
			QMessageBox.warning(QMessageBox(), 'Error', 'Error')

class RemoveSensor(QDialog):
	def __init__(self, *args, **kwargs):
		super(RemoveSensor, self).__init__(*args, **kwargs)

		self.QBtn = QPushButton()
		self.QBtn.setText("Remove")

		self.setWindowTitle("Remove Sensor")
		self.setFixedWidth(300)
		self.setFixedHeight(100)
		self.QBtn.clicked.connect(self.removesensor)
		layout = QVBoxLayout()

		self.listsensor = QComboBox()

		url = requests.get("http://192.168.56.106:5555/containers/json?all=true")
		json1 = json.loads(url.content)

		for sensor in json1:
			for name in sensor['Names']:
				self.listsensor.addItem(name)

		
		layout.addWidget(self.listsensor)

		layout.addWidget(self.QBtn)
		self.setLayout(layout)

	def removesensor(self):

		sensorpilih = ""
		sensorpilih = self.listsensor.itemText(self.listsensor.currentIndex())
		alamat = "http://192.168.56.106:5555/containers" + sensorpilih

		try:
			urlstart = requests.delete(alamat)
			QMessageBox.information(QMessageBox(),'Successful','Successful')
			self.close()
		except Exception:
			QMessageBox.warning(QMessageBox(), 'Error', 'Error')

class AboutDialog(QDialog):
	def __init__(self, *args, **kwargs):
		super(AboutDialog, self).__init__(*args, **kwargs)

		self.setFixedWidth(500)
		self.setFixedHeight(250)

		QBtn = QDialogButtonBox.Ok  
		self.buttonBox = QDialogButtonBox(QBtn)
		self.buttonBox.accepted.connect(self.accept)
		self.buttonBox.rejected.connect(self.reject)

		layout = QVBoxLayout()
		
		self.setWindowTitle("About")
		title = QLabel("Student Record Maintainer In PyQt5")
		font = title.font()
		font.setPointSize(20)
		title.setFont(font)

		labelpic = QLabel()
		pixmap = QPixmap('icon/dexter.jpg')
		pixmap = pixmap.scaledToWidth(275)
		labelpic.setPixmap(pixmap)
		labelpic.setFixedHeight(150)

		layout.addWidget(title)

		layout.addWidget(QLabel("v2.0"))
		layout.addWidget(QLabel("Copyright Okay Dexter 2019"))
		layout.addWidget(labelpic)


		layout.addWidget(self.buttonBox)

		self.setLayout(layout)


class MainWindow(QMainWindow):
	def __init__(self, *args, **kwargs):
		super(MainWindow, self).__init__(*args, **kwargs)
		# self.setWindowIcon(QIcon('icon/g2.png'))  #window icon

		# file_menu = self.menuBar().addMenu("&File")

		# help_menu = self.menuBar().addMenu("&About")
		self.setWindowTitle("Sensor Management")
		self.setMinimumSize(800, 600)

		self.tableWidget = QTableWidget()
		self.setCentralWidget(self.tableWidget)
		self.tableWidget.setAlternatingRowColors(True)
		self.tableWidget.setColumnCount(4)
		self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
		self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
		self.tableWidget.horizontalHeader().setStretchLastSection(True)
		self.tableWidget.verticalHeader().setVisible(False)
		self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
		self.tableWidget.verticalHeader().setStretchLastSection(False)
		self.tableWidget.setHorizontalHeaderLabels(("Names", "Type", "Status", "ID"))

		toolbar = QToolBar()
		toolbar.setMovable(False)
		toolbar.setIconSize(QtCore.QSize(32, 32))
		toolbar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
		self.addToolBar(toolbar)

		statusbar = QStatusBar()
		self.setStatusBar(statusbar)

		btn_ac_refresh = QAction(QIcon("icon/refresh.png"),"Refresh",self)   #refresh icon
		btn_ac_refresh.triggered.connect(self.loaddata)
		btn_ac_refresh.setStatusTip("Refresh Table")
		toolbar.addAction(btn_ac_refresh)

		btn_ac_add = QAction(QIcon("icon/plus.png"), "Add", self)
		# btn_ac_add.triggered.connect(self.add)
		btn_ac_add.setStatusTip("Add Sensor")
		toolbar.addAction(btn_ac_add)

		btn_ac_start = QAction(QIcon("icon/play-button.png"), "Start", self)
		btn_ac_start.triggered.connect(self.start)
		btn_ac_start.setStatusTip("Start Sensor")
		toolbar.addAction(btn_ac_start)

		btn_ac_stop = QAction(QIcon("icon/stop-button.png"), "Stop", self)
		btn_ac_stop.triggered.connect(self.stop)
		btn_ac_stop.setStatusTip("Stop Sensor")
		toolbar.addAction(btn_ac_stop)

		btn_ac_restart = QAction(QIcon("icon/repeat.png"), "Restart", self)
		btn_ac_restart.triggered.connect(self.restart)
		btn_ac_restart.setStatusTip("Restart Sensor")
		toolbar.addAction(btn_ac_restart)

		btn_ac_remove = QAction(QIcon("icon/trash.png"), "Remove", self)
		btn_ac_remove.triggered.connect(self.remove)
		btn_ac_remove.setStatusTip("Remove Sensor")
		toolbar.addAction(btn_ac_remove)

		# adduser_action = QAction(QIcon("icon/add1.jpg"),"Insert Student", self)
		# adduser_action.triggered.connect(self.insert)
		# file_menu.addAction(adduser_action)

		# searchuser_action = QAction(QIcon("icon/s1.png"), "Search Student", self)
		# searchuser_action.triggered.connect(self.search)
		# file_menu.addAction(searchuser_action)

		# deluser_action = QAction(QIcon("icon/d1.png"), "Delete", self)
		# deluser_action.triggered.connect(self.delete)
		# file_menu.addAction(deluser_action)


		# about_action = QAction(QIcon("icon/i1.png"),"Developer", self)  #info icon
		# about_action.triggered.connect(self.about)
		# help_menu.addAction(about_action)

	def loaddata(self):
		url = requests.get("http://192.168.56.106:5555/containers/json?all=true")
		result = json.loads(url.content)

		panjang = len(result)
		self.tableWidget.setRowCount(panjang)

		iter = 0

		for sensor in result:
			for nama in sensor['Names']:
				self.tableWidget.setItem(iter,0, QTableWidgetItem(nama))
			self.tableWidget.setItem(iter,1, QTableWidgetItem(sensor['Image']))
			self.tableWidget.setItem(iter,2, QTableWidgetItem(sensor['Status']))
			self.tableWidget.setItem(iter,3, QTableWidgetItem(sensor['Id']))
			iter+=1

	def insert(self):
		dlg = InsertDialog()
		dlg.exec_()

	def delete(self):
		dlg = DeleteDialog()
		dlg.exec_()

	def start(self):
		dlg = StartSensor()
		dlg.exec_()

	def stop(self):
		dlg = StopSensor()
		dlg.exec_()

	def restart(self):
		dlg = RestartSensor()
		dlg.exec_()

	def remove(self):
		dlg = RemoveSensor()
		dlg.exec_()

	def search(self):
		dlg = SearchDialog()
		dlg.exec_()

	def about(self):
		dlg = AboutDialog()
		dlg.exec_()


app = QApplication(sys.argv)
if(QDialog.Accepted == True):
	window = MainWindow()
	window.show()
	window.loaddata()
sys.exit(app.exec_())
