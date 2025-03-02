
from PyQt5 import QtCore, QtGui, QtWidgets
from src.frontend.admin_table import add_admin

class admin_panel(object):
    def setupUi(self, MainWindow):
        self.MainWindow = MainWindow
        MainWindow.setObjectName("MainWindow")
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
        self.ViewRecords = QtWidgets.QPushButton(self.frame_2)
        self.ViewRecords.setMinimumSize(QtCore.QSize(650, 0))
        self.ViewRecords.setMaximumSize(QtCore.QSize(700, 60))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.ViewRecords.setFont(font)
        self.ViewRecords.setStyleSheet("QPushButton {\n"
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
"}")
        
        self.ViewRecords.setObjectName("ViewRecords")
        self.verticalLayout_4.addWidget(self.ViewRecords)
        self.Add_employee = QtWidgets.QPushButton(self.frame_2)
        self.Add_employee.setMaximumSize(QtCore.QSize(700, 60))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.Add_employee.setFont(font)
        self.Add_employee.setStyleSheet("QPushButton {\n"
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
"}")
        

        self.Add_employee.setObjectName("Add_employee")
        self.verticalLayout_4.addWidget(self.Add_employee)
        self.remove_employee = QtWidgets.QPushButton(self.frame_2)
        self.remove_employee.setMaximumSize(QtCore.QSize(700, 60))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.remove_employee.setFont(font)
        self.remove_employee.setStyleSheet("QPushButton {\n"
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
"}")
        

        self.remove_employee.setObjectName("remove_employee")
        self.verticalLayout_4.addWidget(self.remove_employee)
        self.add_Admin = QtWidgets.QPushButton(self.frame_2)
        self.add_Admin.setMaximumSize(QtCore.QSize(700, 60))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.add_Admin.setFont(font)
        self.add_Admin.setStyleSheet("QPushButton {\n"
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
"}")
        

        self.add_Admin.setObjectName("add_Admin")
        self.verticalLayout_4.addWidget(self.add_Admin)
        self.Logout_B = QtWidgets.QPushButton(self.frame_2)
        self.Logout_B.setMaximumSize(QtCore.QSize(700, 60))
        self.add_Admin.clicked.connect(self.open_add_admin)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.Logout_B.setFont(font)
        self.Logout_B.setStyleSheet("QPushButton {\n"
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
"}")
        
        self.Logout_B.setObjectName("Logout_B")
        self.verticalLayout_4.addWidget(self.Logout_B)
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
        self.ViewRecords.setText(_translate("MainWindow", "View Records"))
        self.Add_employee.setText(_translate("MainWindow", "Add Employee"))
        self.remove_employee.setText(_translate("MainWindow", "Remove Employee"))
        self.add_Admin.setText(_translate("MainWindow", "Add New Admin"))
        self.Logout_B.setText(_translate("MainWindow", "Logout"))

    def open_add_admin(self):
        """Function to open the Add Admin window."""
        self.MainWindow.close()
        self.window = QtWidgets.QMainWindow()  # Create a new window
        self.ui = add_admin()  # Instantiate the add_admin UI
        self.ui.setupUi(self.window)  # Set up the UI
        self.window.show()  # Show the window        


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = admin_panel()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
