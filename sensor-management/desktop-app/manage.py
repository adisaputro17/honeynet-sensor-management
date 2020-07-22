from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtPrintSupport import *
import sys
import requests, json
import pymysql

mydb = pymysql.connect(host="localhost",user="root",password="",db="sensor-management",autocommit=True)

class AgentDialog(QDialog):
	def __init__(self, *args, **kwargs):
		super(AgentDialog, self).__init__(*args, **kwargs)

		self.setWindowIcon(QIcon('icon/agent.png'))
		self.setWindowTitle("Agent")

		self.tableAgent = QTableWidget()
		self.tableAgent.setColumnCount(2)
		self.tableAgent.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
		self.tableAgent.setHorizontalHeaderLabels(("Name", "Address"))
		self.tableAgent.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

		self.loadAgent()

		self.QLoadAgentBtn = QPushButton()
		self.QLoadAgentBtn.setText("Refresh")
		self.QLoadAgentBtn.clicked.connect(self.loadAgent)

		self.QAddAgentBtn = QPushButton()
		self.QAddAgentBtn.setText("Add")
		self.QAddAgentBtn.clicked.connect(self.addAgent)

		self.QRemoveAgentBtn = QPushButton()
		self.QRemoveAgentBtn.setText("Remove")
		self.QRemoveAgentBtn.clicked.connect(self.removeAgent)
 
		self.vBoxLayoutAgent = QVBoxLayout()
		self.vBoxLayoutAgent.addWidget(self.tableAgent)
		self.vBoxLayoutAgent.addWidget(self.QLoadAgentBtn)
		self.vBoxLayoutAgent.addWidget(self.QAddAgentBtn)
		self.vBoxLayoutAgent.addWidget(self.QRemoveAgentBtn)
		self.setLayout(self.vBoxLayoutAgent)

	def loadAgent(self):
		mycursorLoadAgent = mydb.cursor()
		mycursorLoadAgent.execute("select * from agent")
		myresultLoadAgent = mycursorLoadAgent.fetchall()

		banyakdataAgent = len(myresultLoadAgent)
		self.tableAgent.setRowCount(banyakdataAgent)

		iterasiLoadAgent = 0

		for x in myresultLoadAgent:
			self.tableAgent.setItem(iterasiLoadAgent,0, QTableWidgetItem(x[1]))
			self.tableAgent.setItem(iterasiLoadAgent,1, QTableWidgetItem(x[2]))
			iterasiLoadAgent+=1

	def addAgent(self):
		dlg = AddAgent()
		dlg.exec_()
		self.loadAgent()

	def removeAgent(self):
		mycursor = mydb.cursor()
		mycursor.execute("select * from agent")
		myresult = mycursor.fetchall()
		total = len(myresult)

		if (total == 0):
			QMessageBox.warning(QMessageBox(), 'Error', 'Agent is Empty')
		else:
			dlg = RemoveAgent()
			dlg.exec_()
			self.loadAgent()

class AddAgent(QDialog):
	def __init__(self, *args, **kwargs):
		super(AddAgent, self).__init__(*args, **kwargs)

		self.setWindowIcon(QIcon('icon/add.png'))
		self.setWindowTitle("Add new Agent")
		self.setFixedWidth(300)

		layoutAddAgent = QVBoxLayout()

		layoutAddAgent.addWidget(QLabel("Name Agent:"))

		self.nameinputAgent = QLineEdit()
		self.nameinputAgent.setPlaceholderText("Name")
		# self.nameinput.setReadOnly(True);
		layoutAddAgent.addWidget(self.nameinputAgent)

		layoutAddAgent.addWidget(QLabel("IP Address Agent:"))

		self.addressinputAgent = QLineEdit()
		self.addressinputAgent.setPlaceholderText("IP Address")
		layoutAddAgent.addWidget(self.addressinputAgent)

		self.QAddAgentBtn = QPushButton()
		self.QAddAgentBtn.setText("Create Agent")
		self.QAddAgentBtn.clicked.connect(self.addagent)
		layoutAddAgent.addWidget(self.QAddAgentBtn)

		self.setLayout(layoutAddAgent)

	def addagent(self):

		name = ""
		address = ""

		name = self.nameinputAgent.text()
		address = self.addressinputAgent.text()

		try:
			urlCekAlamatAgent = "http://" + address + ":5555/containers/json?all=true"
			cekAlamatAgent = requests.get(urlCekAlamatAgent,timeout=1.0)

			mycursorCekAgent = mydb.cursor()
			mycursorCekAgent.execute("select * from agent where nama=%s or alamat=%s",(name,address))
			hasilCekAgent = len(mycursorCekAgent.fetchall())
			print(hasilCekAgent)

			if(hasilCekAgent == 0):
				mycursorAddAgent = mydb.cursor()
				mycursorAddAgent.execute("insert into agent (nama,alamat) values (%s,%s)",(name,address))
				# mydb.commit()
				QMessageBox.information(QMessageBox(),'Successful','Agent is added successfully')
				self.close()
			else:
				QMessageBox.warning(QMessageBox(), 'Error', 'Agent already')

		except requests.ConnectionError:
			QMessageBox.warning(QMessageBox(), 'Error', 'Could not add Agent')

class RemoveAgent(QDialog):
	def __init__(self, *args, **kwargs):
		super(RemoveAgent, self).__init__(*args, **kwargs)

		self.setWindowIcon(QIcon('icon/remove.png'))
		self.setWindowTitle("Remove Agent")
		self.setFixedWidth(300)

		layoutRemoveAgent = QVBoxLayout()

		layoutRemoveAgent.addWidget(QLabel("Name Agent:"))

		self.comboListRemoveAgent = QComboBox()

		mycursorListRemoveAgent = mydb.cursor()
		mycursorListRemoveAgent.execute("select * from agent")
		myresultListRemoveAgent = mycursorListRemoveAgent.fetchall()

		for x in myresultListRemoveAgent:
			self.comboListRemoveAgent.addItem(x[1])

		self.comboListRemoveAgent.currentIndexChanged.connect(self.indexChangedRemoveAgent)

		layoutRemoveAgent.addWidget(self.comboListRemoveAgent)

		layoutRemoveAgent.addWidget(QLabel("IP Address Agent:"))

		self.lineAddressAgent = QLineEdit()
		self.indexChangedRemoveAgent(self.comboListRemoveAgent.currentIndex())
		self.lineAddressAgent.setPlaceholderText("IP Address")
		self.lineAddressAgent.setReadOnly(True);
		layoutRemoveAgent.addWidget(self.lineAddressAgent)

		self.QRemoveAgentBtn = QPushButton()
		self.QRemoveAgentBtn.setText("Remove Agent")

		self.QRemoveAgentBtn.clicked.connect(self.removeagent)

		layoutRemoveAgent.addWidget(self.QRemoveAgentBtn)

		self.setLayout(layoutRemoveAgent)

	def indexChangedRemoveAgent(self, index):
		self.lineAddressAgent.clear()
		agentSelected = self.comboListRemoveAgent.itemText(index)

		mycursorListAddressAgent = mydb.cursor()
		mycursorListAddressAgent.execute("select alamat from agent where nama = %s",(agentSelected))
		myresultListAddressAgent = mycursorListAddressAgent.fetchall()

		for x in myresultListAddressAgent:
			self.lineAddressAgent.setText(x[0])

	def removeagent(self):
		addressSelected = ""
		addressSelected = self.lineAddressAgent.text()

		mycursorRemoveAgent = mydb.cursor()
		mycursorRemoveAgent.execute("delete from agent where alamat = %s",(addressSelected))
		# mydb.commit()
		QMessageBox.information(QMessageBox(),'Successful','Agent is removed')
		self.close()

class AddSensor(QDialog):
	def __init__(self, *args, **kwargs):
		super(AddSensor, self).__init__(*args, **kwargs)

		self.setWindowIcon(QIcon('icon/add.png'))
		self.setWindowTitle("Add Sensor")
		self.setFixedWidth(300)
		# self.setFixedHeight(100)

		layoutAddSensor = QVBoxLayout()

		layoutAddSensor.addWidget(QLabel("Name Sensor:"))

		self.nameinputSensor = QLineEdit()
		self.nameinputSensor.setPlaceholderText("Name")
		# self.nameinput.setReadOnly(True);
		layoutAddSensor.addWidget(self.nameinputSensor)

		layoutAddSensor.addWidget(QLabel("Type Sensor:"))

		self.typeSensor = QComboBox()
		self.typeSensor.addItem("cowrie")
		self.typeSensor.addItem("dionaea")
		self.typeSensor.addItem("glastopf")
		layoutAddSensor.addWidget(self.typeSensor)


		self.comboListAgentAddSensor = QComboBox()

		layoutAddSensor.addWidget(QLabel("Agent Sensor:"))

		mycursorListAgentAddSensor = mydb.cursor()
		mycursorListAgentAddSensor.execute("select * from agent")
		myresultListAgentAddSensor = mycursorListAgentAddSensor.fetchall()

		for x in myresultListAgentAddSensor:
			self.comboListAgentAddSensor.addItem(x[1] + " |" + x[2]+"|")

		layoutAddSensor.addWidget(self.comboListAgentAddSensor)

		self.QAddSensorBtn = QPushButton()
		self.QAddSensorBtn.setText("Add")

		self.QAddSensorBtn.clicked.connect(self.addsensor)

		layoutAddSensor.addWidget(self.QAddSensorBtn)

		self.setLayout(layoutAddSensor)

	def addsensor(self):
		name = ""
		sensorType = ""
		agent = ""

		name = self.nameinputSensor.text().replace(" ","_")
		sensorType = self.typeSensor.itemText(self.typeSensor.currentIndex())
		agent = self.comboListAgentAddSensor.itemText(self.comboListAgentAddSensor.currentIndex())
		splitAgent = agent.split('|')

		if name:
			print(name)
			print(sensorType)
			print(splitAgent[1])

			urlAddSensor = "http://" + splitAgent[1] + ":5555/containers/create?name=" + name
			print(urlAddSensor)
			myobjCowrie = {
	   "Image": "cowrie/cowrie",
	   "ExposedPorts": {
			   "2222/tcp": {}
	   },
	   "HostConfig": {
		 "PortBindings": { "2222/tcp": [{ "HostPort": "2222" }] }
	  }
  }
			myobjDionaea = {
	   "Image": "ardikabs/dionaea",
	   "ExposedPorts": {
			   "20/tcp": {},
			   "21/tcp": {},
			   "42/tcp": {},
			   "69/udp": {},
			   "135/tcp": {},
			   "443/tcp": {},
			   "445/tcp": {},
			   "1433/tcp": {},
			   "1723/tcp": {},
			   "1883/tcp": {},
			   "3306/tcp": {},
			   "5060/udp": {},
			   "5061/tcp": {},
			   "27017/tcp": {}
	   },
	   "HostConfig": {
		 "PortBindings": { "20/tcp": [{ "HostPort": "20" }],
						   "21/tcp": [{ "HostPort": "21" }],
						   "42/tcp": [{ "HostPort": "42" }],
						   "69/udp": [{ "HostPort": "69" }],
						   "135/tcp": [{ "HostPort": "135" }],
						   "443/tcp": [{ "HostPort": "443" }],
						   "445/tcp": [{ "HostPort": "445" }],
						   "1433/tcp": [{ "HostPort": "1433" }],
						   "1723/tcp": [{ "HostPort": "1723" }],
						   "1883/tcp": [{ "HostPort": "1883" }],
						   "3306/tcp": [{ "HostPort": "3306" }],
						   "5060/udp": [{ "HostPort": "5060" }],
						   "5061/tcp": [{ "HostPort": "5061" }],
						   "27017/tcp": [{ "HostPort": "27017" }] }
	  }
  }
			myobjGlastopf = {
	   "Image": "ardikabs/glastopf",
	   "ExposedPorts": {
			   "80/tcp": {}
	   },
	   "HostConfig": {
		 "PortBindings": { "80/tcp": [{ "HostPort": "80" }] }
	  }
  }

			urlCekSensor = "http://" + splitAgent[1] + ":5555/containers/json?all=true"
			print(urlCekSensor)
			reqCekSensor = requests.get(urlCekSensor)
			resultCekSensor = json.loads(reqCekSensor.content)
			totalSensor = 0

			for sensor in resultCekSensor:
				if sensorType in sensor['Image']:
					totalSensor = 1

			print(totalSensor)

			if totalSensor == 1:
				QMessageBox.warning(QMessageBox(), 'Error', 'Sensor is ready')
			else:
				if sensorType == "cowrie":
					reqAddSensor = requests.post(urlAddSensor,json=myobjCowrie)
					print(reqAddSensor.status_code)
					if reqAddSensor.status_code == 201:
						QMessageBox.information(QMessageBox(),'Successful','Sensor is created successfully')
						self.close()
					else:
						QMessageBox.warning(QMessageBox(), 'Error', 'Could not create sensor')

				if sensorType == "dionaea":
					reqAddSensor = requests.post(urlAddSensor,json=myobjDionaea)
					print(reqAddSensor.status_code)
					if reqAddSensor.status_code == 201:
						QMessageBox.information(QMessageBox(),'Successful','Sensor is created successfully')
						self.close()
					else:
						QMessageBox.warning(QMessageBox(), 'Error', 'Could not create sensor')

				if sensorType == "glastopf":
					reqAddSensor = requests.post(urlAddSensor,json=myobjGlastopf)
					print(reqAddSensor.status_code)
					if reqAddSensor.status_code == 201:
						QMessageBox.information(QMessageBox(),'Successful','Sensor is created successfully')
						self.close()
					else:
						QMessageBox.warning(QMessageBox(), 'Error', 'Could not create sensor')
		else:
			QMessageBox.warning(QMessageBox(), 'Error', 'Name is Empty')

class StartSensor(QDialog):
	def __init__(self, *args, **kwargs):
		super(StartSensor, self).__init__(*args, **kwargs)

		self.setWindowIcon(QIcon('icon/start.png'))
		self.setWindowTitle("Start Sensor")
		self.setFixedWidth(300)
		# self.setFixedHeight(100)

		layoutStartSensor = QVBoxLayout()

		layoutStartSensor.addWidget(QLabel("Agent:"))

		self.comboListAgentStartSensor = QComboBox()

		mycursorListStartSensor = mydb.cursor()
		mycursorListStartSensor.execute("select * from agent")
		myresultListStartSensor = mycursorListStartSensor.fetchall()

		for x in myresultListStartSensor:
			self.comboListAgentStartSensor.addItem(x[1] + " |" + x[2]+"|")

		self.comboListAgentStartSensor.currentIndexChanged.connect(self.indexChangedStartSensor)

		layoutStartSensor.addWidget(self.comboListAgentStartSensor)

		layoutStartSensor.addWidget(QLabel("Sensor:"))

		self.comboListStartSensor = QComboBox()
		self.indexChangedStartSensor(self.comboListAgentStartSensor.currentIndex())
		layoutStartSensor.addWidget(self.comboListStartSensor)

		self.QStartSensorBtn = QPushButton()
		self.QStartSensorBtn.setText("Start")
		layoutStartSensor.addWidget(self.QStartSensorBtn)

		self.QStartSensorBtn.clicked.connect(self.startsensor)
				
		self.setLayout(layoutStartSensor)

	def indexChangedStartSensor(self, index):
		self.comboListStartSensor.clear()
		agentSelected = self.comboListAgentStartSensor.itemText(index)
		splitAgent = agentSelected.split('|')

		urlSensorSelected = "http://" + splitAgent[1] + ":5555/containers/json?all=true"
		reqSensorSelected = requests.get(urlSensorSelected)
		jsonSensorSelected = json.loads(reqSensorSelected.content)

		for sensor in jsonSensorSelected:
			for nama in sensor['Names']:
				splitNama = nama.split('/')
				self.comboListStartSensor.addItem(splitNama[1])

	def startsensor(self):
		agentSelected = self.comboListAgentStartSensor.itemText(self.comboListAgentStartSensor.currentIndex())
		splitAgent = agentSelected.split('|')
		sensorSelected = self.comboListStartSensor.itemText(self.comboListStartSensor.currentIndex())

		urlStartSensor = "http://" + splitAgent[1] + ":5555/containers/" + sensorSelected + "/start"
		reqStartSensor = requests.post(urlStartSensor)

		if reqStartSensor.status_code == 204:
			QMessageBox.information(QMessageBox(),'Successful','Sensor is started successfully')
			self.close()
		else:
			QMessageBox.warning(QMessageBox(), 'Error', 'Sensor is running')

class StopSensor(QDialog):
	def __init__(self, *args, **kwargs):
		super(StopSensor, self).__init__(*args, **kwargs)

		self.setWindowIcon(QIcon('icon/stop.png'))
		self.setWindowTitle("Stop Sensor")
		self.setFixedWidth(300)
		# self.setFixedHeight(100)

		layoutStopSensor = QVBoxLayout()

		layoutStopSensor.addWidget(QLabel("Agent:"))

		self.comboListAgentStopSensor = QComboBox()

		mycursorListStopSensor = mydb.cursor()
		mycursorListStopSensor.execute("select * from agent")
		myresultListStopSensor = mycursorListStopSensor.fetchall()

		for x in myresultListStopSensor:
			self.comboListAgentStopSensor.addItem(x[1] + " |" + x[2]+"|")

		self.comboListAgentStopSensor.currentIndexChanged.connect(self.indexChangedStopSensor)

		layoutStopSensor.addWidget(self.comboListAgentStopSensor)

		layoutStopSensor.addWidget(QLabel("Sensor:"))

		self.comboListStopSensor = QComboBox()
		self.indexChangedStopSensor(self.comboListAgentStopSensor.currentIndex())
		layoutStopSensor.addWidget(self.comboListStopSensor)

		self.QStopSensorBtn = QPushButton()
		self.QStopSensorBtn.setText("Stop")
		layoutStopSensor.addWidget(self.QStopSensorBtn)

		self.QStopSensorBtn.clicked.connect(self.stopsensor)
				
		self.setLayout(layoutStopSensor)

	def indexChangedStopSensor(self, index):
		self.comboListStopSensor.clear()
		agentSelected = self.comboListAgentStopSensor.itemText(index)
		splitAgent = agentSelected.split('|')

		urlSensorSelected = "http://" + splitAgent[1] + ":5555/containers/json"
		reqSensorSelected = requests.get(urlSensorSelected)
		jsonSensorSelected = json.loads(reqSensorSelected.content)

		for sensor in jsonSensorSelected:
			for nama in sensor['Names']:
				splitNama = nama.split('/')
				self.comboListStopSensor.addItem(splitNama[1])

	def stopsensor(self):
		agentSelected = self.comboListAgentStopSensor.itemText(self.comboListAgentStopSensor.currentIndex())
		splitAgent = agentSelected.split('|')
		sensorSelected = self.comboListStopSensor.itemText(self.comboListStopSensor.currentIndex())

		urlStopSensor = "http://" + splitAgent[1] + ":5555/containers/" + sensorSelected + "/stop"
		reqStopSensor = requests.post(urlStopSensor)

		if reqStopSensor.status_code == 204:
			QMessageBox.information(QMessageBox(),'Successful','Sensor is stopped successfully')
			self.close()
		else:
			QMessageBox.warning(QMessageBox(), 'Error', 'Sensor is not running')

class RestartSensor(QDialog):
	def __init__(self, *args, **kwargs):
		super(RestartSensor, self).__init__(*args, **kwargs)

		self.setWindowIcon(QIcon('icon/restart.png'))
		self.setWindowTitle("Restart Sensor")
		self.setFixedWidth(300)
		# self.setFixedHeight(100)

		layoutRestartSensor = QVBoxLayout()

		layoutRestartSensor.addWidget(QLabel("Agent:"))

		self.comboListAgentRestartSensor = QComboBox()

		mycursorListRestartSensor = mydb.cursor()
		mycursorListRestartSensor.execute("select * from agent")
		myresultListRestartSensor = mycursorListRestartSensor.fetchall()

		for x in myresultListRestartSensor:
			self.comboListAgentRestartSensor.addItem(x[1] + " |" + x[2]+"|")

		self.comboListAgentRestartSensor.currentIndexChanged.connect(self.indexChangedRestartSensor)

		layoutRestartSensor.addWidget(self.comboListAgentRestartSensor)

		layoutRestartSensor.addWidget(QLabel("Sensor:"))

		self.comboListRestartSensor = QComboBox()
		self.indexChangedRestartSensor(self.comboListAgentRestartSensor.currentIndex())
		layoutRestartSensor.addWidget(self.comboListRestartSensor)

		self.QRestartSensorBtn = QPushButton()
		self.QRestartSensorBtn.setText("Restart")
		layoutRestartSensor.addWidget(self.QRestartSensorBtn)

		self.QRestartSensorBtn.clicked.connect(self.restartsensor)
				
		self.setLayout(layoutRestartSensor)

	def indexChangedRestartSensor(self, index):
		self.comboListRestartSensor.clear()
		agentSelected = self.comboListAgentRestartSensor.itemText(index)
		splitAgent = agentSelected.split('|')

		urlSensorSelected = "http://" + splitAgent[1] + ":5555/containers/json"
		reqSensorSelected = requests.get(urlSensorSelected)
		jsonSensorSelected = json.loads(reqSensorSelected.content)

		for sensor in jsonSensorSelected:
			for nama in sensor['Names']:
				splitNama = nama.split('/')
				self.comboListRestartSensor.addItem(splitNama[1])

	def restartsensor(self):
		agentSelected = self.comboListAgentRestartSensor.itemText(self.comboListAgentRestartSensor.currentIndex())
		splitAgent = agentSelected.split('|')
		sensorSelected = self.comboListRestartSensor.itemText(self.comboListRestartSensor.currentIndex())

		urlRestartSensor = "http://" + splitAgent[1] + ":5555/containers/" + sensorSelected + "/restart"
		reqRestartSensor = requests.post(urlRestartSensor)

		if reqRestartSensor.status_code == 204:
			QMessageBox.information(QMessageBox(),'Successful','Sensor is restarted successfully')
			self.close()
		else:
			QMessageBox.warning(QMessageBox(), 'Error', 'Sensor is not running')

class RemoveSensor(QDialog):
	def __init__(self, *args, **kwargs):
		super(RemoveSensor, self).__init__(*args, **kwargs)

		self.setWindowIcon(QIcon('icon/remove.png'))
		self.setWindowTitle("Remove Sensor")
		self.setFixedWidth(300)
		# self.setFixedHeight(100)

		layoutRemoveSensor = QVBoxLayout()

		layoutRemoveSensor.addWidget(QLabel("Agent:"))

		self.comboListAgentRemoveSensor = QComboBox()

		mycursorListRemoveSensor = mydb.cursor()
		mycursorListRemoveSensor.execute("select * from agent")
		myresultListRemoveSensor = mycursorListRemoveSensor.fetchall()

		for x in myresultListRemoveSensor:
			self.comboListAgentRemoveSensor.addItem(x[1] + " |" + x[2]+"|")

		self.comboListAgentRemoveSensor.currentIndexChanged.connect(self.indexChangedRemoveSensor)

		layoutRemoveSensor.addWidget(self.comboListAgentRemoveSensor)

		layoutRemoveSensor.addWidget(QLabel("Sensor:"))

		self.comboListRemoveSensor = QComboBox()
		self.indexChangedRemoveSensor(self.comboListAgentRemoveSensor.currentIndex())
		layoutRemoveSensor.addWidget(self.comboListRemoveSensor)

		self.QRemoveSensorBtn = QPushButton()
		self.QRemoveSensorBtn.setText("Remove")
		layoutRemoveSensor.addWidget(self.QRemoveSensorBtn)

		self.QRemoveSensorBtn.clicked.connect(self.removesensor)
				
		self.setLayout(layoutRemoveSensor)

	def indexChangedRemoveSensor(self, index):
		self.comboListRemoveSensor.clear()
		agentSelected = self.comboListAgentRemoveSensor.itemText(index)
		splitAgent = agentSelected.split('|')

		urlSensorSelected = "http://" + splitAgent[1] + ":5555/containers/json?all=true"
		reqSensorSelected = requests.get(urlSensorSelected)
		jsonSensorSelected = json.loads(reqSensorSelected.content)

		for sensor in jsonSensorSelected:
			for nama in sensor['Names']:
				splitNama = nama.split('/')
				self.comboListRemoveSensor.addItem(splitNama[1])

	def removesensor(self):
		agentSelected = self.comboListAgentRemoveSensor.itemText(self.comboListAgentRemoveSensor.currentIndex())
		splitAgent = agentSelected.split('|')
		sensorSelected = self.comboListRemoveSensor.itemText(self.comboListRemoveSensor.currentIndex())

		urlRemoveSensor = "http://" + splitAgent[1] + ":5555/containers/" + sensorSelected
		reqRemoveSensor = requests.delete(urlRemoveSensor)

		if reqRemoveSensor.status_code == 204:
			QMessageBox.information(QMessageBox(),'Successful','Sensor is removed successfully')
			self.close()
		else:
			QMessageBox.warning(QMessageBox(), 'Error', 'Sensor is running')

class ChangePassword(QDialog):
	def __init__(self, *args, **kwargs):
		super(ChangePassword, self).__init__(*args, **kwargs)

		self.setWindowIcon(QIcon('icon/password.png'))
		self.setWindowTitle("Change Password")
		self.setFixedWidth(300)

		layoutChangePassword = QVBoxLayout()

		layoutChangePassword.addWidget(QLabel("Current Password:"))

		self.PasswordInput = QLineEdit()
		self.PasswordInput.setPlaceholderText("Current Password")
		self.PasswordInput.setEchoMode(QtWidgets.QLineEdit.Password)
		layoutChangePassword.addWidget(self.PasswordInput)

		layoutChangePassword.addWidget(QLabel("New Password:"))

		self.NewPasswordInput = QLineEdit()
		self.NewPasswordInput.setPlaceholderText("New Password")
		self.NewPasswordInput.setEchoMode(QtWidgets.QLineEdit.Password)
		layoutChangePassword.addWidget(self.NewPasswordInput)

		layoutChangePassword.addWidget(QLabel("Verify Password:"))

		self.NewPasswordInput1 = QLineEdit()
		self.NewPasswordInput1.setPlaceholderText("Verify Password")
		self.NewPasswordInput1.setEchoMode(QtWidgets.QLineEdit.Password)
		layoutChangePassword.addWidget(self.NewPasswordInput1)

		self.QPasswordBtn = QPushButton()
		self.QPasswordBtn.setText("Change Password")
		self.QPasswordBtn.clicked.connect(self.changepassword)
		layoutChangePassword.addWidget(self.QPasswordBtn)

		self.setLayout(layoutChangePassword)

	def changepassword(self):
		password = self.PasswordInput.text()
		newpassword = self.NewPasswordInput.text()
		newpassword1 = self.NewPasswordInput1.text()

		mycursorNewPassword = mydb.cursor()
		mycursorNewPassword.execute("select * from admin where password = %s",(password))
		myresultNewPassword = mycursorNewPassword.fetchall()

		if len(myresultNewPassword) > 0:

			if newpassword == newpassword1:
				mycursorNewPassword.execute("update admin set password = %s",(newpassword))
				QMessageBox.information(QMessageBox(),'Successful','Password is Changed successfully')
				self.close()
			else:
				QMessageBox.warning(QMessageBox(), 'Error', 'Invalid Verify Password')
		else:
			QMessageBox.warning(QMessageBox(), 'Error', 'Invalid Password')

class LoginDialog(QDialog):
	def __init__(self, *args, **kwargs):
		super(LoginDialog, self).__init__(*args, **kwargs)

		self.setWindowIcon(QIcon('icon/login.png'))
		self.setWindowTitle("Login")
		self.setFixedWidth(300)

		layoutLoginDialog = QVBoxLayout()

		layoutLoginDialog.addWidget(QLabel("Username:"))

		self.UsernameInput = QLineEdit()
		self.UsernameInput.setPlaceholderText("Username")
		layoutLoginDialog.addWidget(self.UsernameInput)

		layoutLoginDialog.addWidget(QLabel("Password:"))

		self.PasswordInput = QLineEdit()
		self.PasswordInput.setPlaceholderText("Password")
		self.PasswordInput.setEchoMode(QtWidgets.QLineEdit.Password)
		layoutLoginDialog.addWidget(self.PasswordInput)

		self.QLoginBtn = QPushButton()
		self.QLoginBtn.setText("Login")
		self.QLoginBtn.clicked.connect(self.login)
		layoutLoginDialog.addWidget(self.QLoginBtn)

		self.setLayout(layoutLoginDialog)

	def login(self):
		username = self.UsernameInput.text()
		password = self.PasswordInput.text()

		mycursorLogin = mydb.cursor()
		mycursorLogin.execute("select * from admin where username = %s and password = %s",(username,password))
		myresultLogin = mycursorLogin.fetchall()

		if len(myresultLogin) > 0:
			QMessageBox.information(QMessageBox(),'Successful','Login is successfully')
			self.close()
			self.mainwindow = MainWindow()
			self.mainwindow.show()
		else:
			QMessageBox.warning(QMessageBox(), 'Error', 'Invalid Username or Password')

class MainWindow(QMainWindow):
	def __init__(self, *args, **kwargs):
		super(MainWindow, self).__init__(*args, **kwargs)
		self.setWindowIcon(QIcon('icon/docker.png'))

		self.setWindowTitle("Sensor Management")
		self.setMinimumSize(800, 600)

		self.tableWidget = QTableWidget()
		self.setCentralWidget(self.tableWidget)
		self.tableWidget.setAlternatingRowColors(True)
		self.tableWidget.setColumnCount(5)
		self.tableWidget.setRowCount(100)
		self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
		self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
		self.tableWidget.horizontalHeader().setStretchLastSection(True)
		self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
		# self.tableWidget.verticalHeader().setVisible(False)
		self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
		self.tableWidget.verticalHeader().setStretchLastSection(False)
		# self.tableWidget.setHorizontalHeaderLabels(("Names","Agent","IP Address", "Type", "Status", "ID"))

		self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

		self.loaddata()

		timer = QtCore.QTimer(self)
		timer.start(10000)	#millisecond 
		timer.timeout.connect(self.loaddata)

		toolbar = QToolBar()
		toolbar.setMovable(False)
		toolbar.setIconSize(QtCore.QSize(40, 40))
		toolbar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
		# toolbar.setStyleSheet("background-color: rgb(39, 174, 96);")
		self.addToolBar(toolbar)

		statusbar = QStatusBar()
		self.setStatusBar(statusbar)

		btn_ac_agent = QAction(QIcon("icon/agent.png"),"Agent",self)
		btn_ac_agent.triggered.connect(self.agent)
		btn_ac_agent.setStatusTip("Agent")
		toolbar.addAction(btn_ac_agent)

		btn_ac_refresh = QAction(QIcon("icon/refresh.png"),"Refresh",self)
		btn_ac_refresh.triggered.connect(self.loaddata)
		btn_ac_refresh.setStatusTip("Refresh Table")
		toolbar.addAction(btn_ac_refresh)

		btn_ac_add = QAction(QIcon("icon/add.png"), "Add", self)
		btn_ac_add.triggered.connect(self.add)
		btn_ac_add.setStatusTip("Add Sensor")
		toolbar.addAction(btn_ac_add)

		btn_ac_start = QAction(QIcon("icon/start.png"), "Start", self)
		btn_ac_start.triggered.connect(self.start)
		btn_ac_start.setStatusTip("Start Sensor")
		toolbar.addAction(btn_ac_start)

		btn_ac_stop = QAction(QIcon("icon/stop.png"), "Stop", self)
		btn_ac_stop.triggered.connect(self.stop)
		btn_ac_stop.setStatusTip("Stop Sensor")
		toolbar.addAction(btn_ac_stop)

		btn_ac_restart = QAction(QIcon("icon/restart.png"), "Restart", self)
		btn_ac_restart.triggered.connect(self.restart)
		btn_ac_restart.setStatusTip("Restart Sensor")
		toolbar.addAction(btn_ac_restart)

		btn_ac_remove = QAction(QIcon("icon/remove.png"), "Remove", self)
		btn_ac_remove.triggered.connect(self.remove)
		btn_ac_remove.setStatusTip("Remove Sensor")
		toolbar.addAction(btn_ac_remove)

		btn_ac_password = QAction(QIcon("icon/password.png"), "Change Password", self)
		btn_ac_password.triggered.connect(self.password)
		btn_ac_password.setStatusTip("Change Password")
		toolbar.addAction(btn_ac_password)

		btn_ac_logout = QAction(QIcon("icon/logout.png"), "Logout", self)
		btn_ac_logout.triggered.connect(self.logout)
		btn_ac_logout.setStatusTip("Logout")
		toolbar.addAction(btn_ac_logout)

	def agent(self):
		dlg = AgentDialog()
		dlg.exec_()
		self.loaddata()

	def loaddata(self):
		self.tableWidget.clear()

		self.tableWidget.setHorizontalHeaderLabels(("Names","Agent","IP Address", "Type", "Status"))

		mycursorLoadData = mydb.cursor()
		mycursorLoadData.execute("select * from agent")
		myresultLoadData = mycursorLoadData.fetchall()

		iterasiLoadData = 0

		for x in myresultLoadData:
			alamat = "http://" + x[2] + ":5555/containers/json?all=true"
			# print(alamat)
			req = requests.get(alamat)
			result = json.loads(req.content)

			for sensor in result:
				splitImage = sensor['Image'].split('/')
				splitStatus = sensor['Status'].split(' ')
				for nama in sensor['Names']:
					splitNama = nama.split('/')
					self.tableWidget.setItem(iterasiLoadData,0, QTableWidgetItem(splitNama[1]))
				self.tableWidget.setItem(iterasiLoadData,3, QTableWidgetItem(splitImage[1]))
				
				# self.tableWidget.setItem(iterasiLoadData,5, QTableWidgetItem(sensor['Id']))
				self.tableWidget.setItem(iterasiLoadData,1, QTableWidgetItem(x[1]))
				self.tableWidget.setItem(iterasiLoadData,2, QTableWidgetItem(x[2]))
				if "running" in sensor['State']:
					self.tableWidget.setItem(iterasiLoadData,4, QTableWidgetItem(sensor['Status']))
					self.tableWidget.item(iterasiLoadData, 4).setForeground(QtGui.QColor(0, 200, 0))
					# self.tableWidget.item(iterasiLoadData, 4).setBackground(QtGui.QColor(0, 200, 0))
				elif "exited" in sensor['State']:
					self.tableWidget.setItem(iterasiLoadData,4, QTableWidgetItem(splitStatus[0] + " " + splitStatus[2] + " " + splitStatus[3] + " " + splitStatus[4]))
					self.tableWidget.item(iterasiLoadData, 4).setForeground(QtGui.QColor(255, 0, 0))
				else:
					self.tableWidget.setItem(iterasiLoadData,4, QTableWidgetItem(sensor['Status']))
				iterasiLoadData+=1

	def add(self):

		mycursor = mydb.cursor()
		mycursor.execute("select * from agent")
		myresult = mycursor.fetchall()
		total = len(myresult)

		if (total == 0):
			QMessageBox.warning(QMessageBox(), 'Error', 'Agent is Empty')
		else:
			dlg = AddSensor()
			dlg.exec_()
			self.loaddata()

	def start(self):

		mycursor = mydb.cursor()
		mycursor.execute("select * from agent")
		myresult = mycursor.fetchall()
		total = len(myresult)

		if (total == 0):
			QMessageBox.warning(QMessageBox(), 'Error', 'Agent is Empty')
		else:
			dlg = StartSensor()
			dlg.exec_()
			self.loaddata()

	def stop(self):

		mycursor = mydb.cursor()
		mycursor.execute("select * from agent")
		myresult = mycursor.fetchall()
		total = len(myresult)

		if (total == 0):
			QMessageBox.warning(QMessageBox(), 'Error', 'Agent is Empty')
		else:
			dlg = StopSensor()
			dlg.exec_()
			self.loaddata()

	def restart(self):
		mycursor = mydb.cursor()
		mycursor.execute("select * from agent")
		myresult = mycursor.fetchall()
		total = len(myresult)

		if (total == 0):
			QMessageBox.warning(QMessageBox(), 'Error', 'Agent is Empty')
		else:
			dlg = RestartSensor()
			dlg.exec_()
			self.loaddata()

	def remove(self):
		mycursor = mydb.cursor()
		mycursor.execute("select * from agent")
		myresult = mycursor.fetchall()
		total = len(myresult)

		if (total == 0):
			QMessageBox.warning(QMessageBox(), 'Error', 'Agent is Empty')
		else:
			dlg = RemoveSensor()
			dlg.exec_()
			self.loaddata()

	def password(self):
		dlg = ChangePassword()
		dlg.exec_()

	def logout(self):
		self.close()
		self.loginwindow = LoginDialog()
		self.loginwindow.show()

font = QFont("Arial", 10)
app = QApplication(sys.argv)
app.setFont(font)
if(QDialog.Accepted == True):
	window = LoginDialog()
	window.show()
	# window.loaddata()
sys.exit(app.exec_())
