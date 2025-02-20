from PyQt5 import QtCore, QtGui, QtWidgets


class admin_panel:
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Admin Panel")
        MainWindow.resize(883, 676)
        MainWindow.setStyleSheet("background-color: rgb(8, 39, 79);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setMinimumSize(QtCore.QSize(0, 0))
        self.frame.setMaximumSize(QtCore.QSize(480, 100))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setMaximumSize(QtCore.QSize(800, 16777215))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(36)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet("color: rgb(255, 255, 255);")
        self.label.setObjectName("label")
        self.verticalLayout_3.addWidget(self.label)
        self.verticalLayout_2.addWidget(self.frame, 0, QtCore.Qt.AlignHCenter)
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setMinimumSize(QtCore.QSize(700, 0))
        self.frame_2.setMaximumSize(QtCore.QSize(700, 16777215))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.pushButton = QtWidgets.QPushButton(self.frame_2)
        self.pushButton.setMinimumSize(QtCore.QSize(650, 0))
        self.pushButton.setMaximumSize(QtCore.QSize(700, 60))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet(
            "QPushButton {\n"
            "    background-color: rgb(75, 152, 61); \n"
            "    color: rgb(255, 255, 255);\n"
            "}\n"
            "\n"
            "QPushButton:hover {\n"
            "    background-color: rgb(75, 160, 61); \n"
            "}\n"
            "\n"
            "QPushButton:pressed {\n"
            "    background-color: rgb(75, 180, 61);\n"
            "}"
        )
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_4.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.frame_2)
        self.pushButton_2.setMaximumSize(QtCore.QSize(700, 60))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setStyleSheet(
            "QPushButton {\n"
            "    background-color: rgb(75, 152, 61); \n"
            "    color: rgb(255, 255, 255);\n"
            "}\n"
            "\n"
            "QPushButton:hover {\n"
            "    background-color: rgb(75, 160, 61); \n"
            "}\n"
            "\n"
            "QPushButton:pressed {\n"
            "    background-color: rgb(75, 180, 61);\n"
            "}"
        )
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout_4.addWidget(self.pushButton_2)
        self.pushButton_3 = QtWidgets.QPushButton(self.frame_2)
        self.pushButton_3.setMaximumSize(QtCore.QSize(700, 60))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setStyleSheet(
            "QPushButton {\n"
            "    background-color: rgb(75, 152, 61); \n"
            "    color: rgb(255, 255, 255);\n"
            "}\n"
            "\n"
            "QPushButton:hover {\n"
            "    background-color: rgb(75, 160, 61); \n"
            "}\n"
            "\n"
            "QPushButton:pressed {\n"
            "    background-color: rgb(75, 180, 61);\n"
            "}"
        )
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout_4.addWidget(self.pushButton_3)
        self.pushButton_4 = QtWidgets.QPushButton(self.frame_2)
        self.pushButton_4.setMaximumSize(QtCore.QSize(700, 60))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setStyleSheet(
            "QPushButton {\n"
            "    background-color: rgb(75, 152, 61); \n"
            "    color: rgb(255, 255, 255);\n"
            "}\n"
            "\n"
            "QPushButton:hover {\n"
            "    background-color: rgb(75, 160, 61); \n"
            "}\n"
            "\n"
            "QPushButton:pressed {\n"
            "    background-color: rgb(75, 180, 61);\n"
            "}"
        )
        self.pushButton_4.setObjectName("pushButton_4")
        self.verticalLayout_4.addWidget(self.pushButton_4)
        self.pushButton_5 = QtWidgets.QPushButton(self.frame_2)
        self.pushButton_5.setMaximumSize(QtCore.QSize(700, 60))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_5.setFont(font)
        self.pushButton_5.setStyleSheet(
            "QPushButton {\n"
            "    background-color: rgb(75, 152, 61); \n"
            "    color: rgb(255, 255, 255);\n"
            "}\n"
            "\n"
            "QPushButton:hover {\n"
            "    background-color: rgb(75, 160, 61); \n"
            "}\n"
            "\n"
            "QPushButton:pressed {\n"
            "    background-color: rgb(75, 180, 61);\n"
            "}"
        )
        self.pushButton_5.setObjectName("pushButton_5")
        self.verticalLayout_4.addWidget(self.pushButton_5)
        self.verticalLayout_2.addWidget(self.frame_2, 0, QtCore.Qt.AlignHCenter)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 883, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "ADMIN CONTROLS"))
        self.pushButton.setText(_translate("MainWindow", "View Records"))
        self.pushButton_2.setText(_translate("MainWindow", "Add Employee"))
        self.pushButton_3.setText(_translate("MainWindow", "Remove Employee"))
        self.pushButton_4.setText(_translate("MainWindow", "Add New Admin"))
        self.pushButton_5.setText(_translate("MainWindow", "Logout"))


