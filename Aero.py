from PyQt5 import QtCore, QtGui, QtWidgets
import logging
from Density_Calculator import main_density
from Dynamic_viscosity_Calculator import dynamic_viscosity
from Reynolds_Number_Calculator import main_reynolds

# Configure logging to log everything (DEBUG level and above) and write to a file
logging.basicConfig(filename='log.txt', filemode='a', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Version of the script
__version__ = "0.03"


logging.info(f"Starting Insert Data to Shop Floor script v{__version__}")

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1231, 892)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.altitude_label = QtWidgets.QLabel(self.centralwidget)
        self.altitude_label.setGeometry(QtCore.QRect(50, 120, 220, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.altitude_label.setFont(font)
        self.altitude_label.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.altitude_label.setFrameShape(QtWidgets.QFrame.Box)
        self.altitude_label.setLineWidth(2)
        self.altitude_label.setAlignment(QtCore.Qt.AlignCenter)
        self.altitude_label.setObjectName("altitude_label")
        self.altitude_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.altitude_lineEdit.setGeometry(QtCore.QRect(280, 120, 181, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.altitude_lineEdit.setFont(font)
        self.altitude_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.altitude_lineEdit.setObjectName("altitude_lineEdit")
        self.humidity_label = QtWidgets.QLabel(self.centralwidget)
        self.humidity_label.setGeometry(QtCore.QRect(50, 180, 220, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.humidity_label.setFont(font)
        self.humidity_label.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.humidity_label.setFrameShape(QtWidgets.QFrame.Box)
        self.humidity_label.setLineWidth(2)
        self.humidity_label.setAlignment(QtCore.Qt.AlignCenter)
        self.humidity_label.setObjectName("humidity_label")
        self.humidity_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.humidity_lineEdit.setGeometry(QtCore.QRect(280, 180, 181, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.humidity_lineEdit.setFont(font)
        self.humidity_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.humidity_lineEdit.setObjectName("humidity_lineEdit")
        self.barometric_pressure_label = QtWidgets.QLabel(self.centralwidget)
        self.barometric_pressure_label.setGeometry(QtCore.QRect(50, 240, 220, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.barometric_pressure_label.setFont(font)
        self.barometric_pressure_label.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.barometric_pressure_label.setFrameShape(QtWidgets.QFrame.Box)
        self.barometric_pressure_label.setLineWidth(2)
        self.barometric_pressure_label.setAlignment(QtCore.Qt.AlignCenter)
        self.barometric_pressure_label.setObjectName("barometric_pressure_label")
        self.barometric_pressure_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.barometric_pressure_lineEdit.setGeometry(QtCore.QRect(280, 240, 181, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.barometric_pressure_lineEdit.setFont(font)
        self.barometric_pressure_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.barometric_pressure_lineEdit.setObjectName("barometric_pressure_lineEdit")
        self.density_label = QtWidgets.QLabel(self.centralwidget)
        self.density_label.setGeometry(QtCore.QRect(590, 120, 220, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.density_label.setFont(font)
        self.density_label.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.density_label.setFrameShape(QtWidgets.QFrame.Box)
        self.density_label.setLineWidth(2)
        self.density_label.setAlignment(QtCore.Qt.AlignCenter)
        self.density_label.setObjectName("density_label")
        self.density_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.density_lineEdit.setGeometry(QtCore.QRect(820, 120, 181, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.density_lineEdit.setFont(font)
        self.density_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.density_lineEdit.setReadOnly(True)
        self.density_lineEdit.setObjectName("density_lineEdit")
        self.temperature_label = QtWidgets.QLabel(self.centralwidget)
        self.temperature_label.setGeometry(QtCore.QRect(50, 300, 220, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.temperature_label.setFont(font)
        self.temperature_label.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.temperature_label.setFrameShape(QtWidgets.QFrame.Box)
        self.temperature_label.setLineWidth(2)
        self.temperature_label.setAlignment(QtCore.Qt.AlignCenter)
        self.temperature_label.setObjectName("temperature_label")
        self.temperature_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.temperature_lineEdit.setGeometry(QtCore.QRect(280, 300, 181, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.temperature_lineEdit.setFont(font)
        self.temperature_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.temperature_lineEdit.setObjectName("temperature_lineEdit")
        self.dynamic_viscocity_label = QtWidgets.QLabel(self.centralwidget)
        self.dynamic_viscocity_label.setGeometry(QtCore.QRect(590, 180, 220, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.dynamic_viscocity_label.setFont(font)
        self.dynamic_viscocity_label.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.dynamic_viscocity_label.setFrameShape(QtWidgets.QFrame.Box)
        self.dynamic_viscocity_label.setLineWidth(2)
        self.dynamic_viscocity_label.setAlignment(QtCore.Qt.AlignCenter)
        self.dynamic_viscocity_label.setObjectName("dynamic_viscocity_label")
        self.dynamic_viscocity_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.dynamic_viscocity_lineEdit.setGeometry(QtCore.QRect(820, 180, 181, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.dynamic_viscocity_lineEdit.setFont(font)
        self.dynamic_viscocity_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.dynamic_viscocity_lineEdit.setReadOnly(True)
        self.dynamic_viscocity_lineEdit.setObjectName("dynamic_viscocity_lineEdit")
        self.velocity_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.velocity_lineEdit.setGeometry(QtCore.QRect(280, 360, 181, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.velocity_lineEdit.setFont(font)
        self.velocity_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.velocity_lineEdit.setObjectName("velocity_lineEdit")
        self.velocity_label = QtWidgets.QLabel(self.centralwidget)
        self.velocity_label.setGeometry(QtCore.QRect(50, 360, 220, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.velocity_label.setFont(font)
        self.velocity_label.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.velocity_label.setFrameShape(QtWidgets.QFrame.Box)
        self.velocity_label.setLineWidth(2)
        self.velocity_label.setAlignment(QtCore.Qt.AlignCenter)
        self.velocity_label.setObjectName("velocity_label")
        self.chord_length_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.chord_length_lineEdit.setGeometry(QtCore.QRect(280, 420, 181, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.chord_length_lineEdit.setFont(font)
        self.chord_length_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.chord_length_lineEdit.setObjectName("chord_length_lineEdit")
        self.chord_length_label = QtWidgets.QLabel(self.centralwidget)
        self.chord_length_label.setGeometry(QtCore.QRect(50, 420, 220, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.chord_length_label.setFont(font)
        self.chord_length_label.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.chord_length_label.setFrameShape(QtWidgets.QFrame.Box)
        self.chord_length_label.setLineWidth(2)
        self.chord_length_label.setAlignment(QtCore.Qt.AlignCenter)
        self.chord_length_label.setObjectName("chord_length_label")
        self.reynolds_number_label = QtWidgets.QLabel(self.centralwidget)
        self.reynolds_number_label.setGeometry(QtCore.QRect(590, 240, 220, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.reynolds_number_label.setFont(font)
        self.reynolds_number_label.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.reynolds_number_label.setFrameShape(QtWidgets.QFrame.Box)
        self.reynolds_number_label.setLineWidth(2)
        self.reynolds_number_label.setAlignment(QtCore.Qt.AlignCenter)
        self.reynolds_number_label.setObjectName("reynolds_number_label")
        self.reynolds_number_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.reynolds_number_lineEdit.setGeometry(QtCore.QRect(820, 240, 181, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.reynolds_number_lineEdit.setFont(font)
        self.reynolds_number_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.reynolds_number_lineEdit.setReadOnly(True)
        self.reynolds_number_lineEdit.setObjectName("reynolds_number_lineEdit")
        self.calculate_density_pushButton = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: self.calculate_density())
        self.calculate_density_pushButton.setGeometry(QtCore.QRect(590, 300, 300, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.calculate_density_pushButton.setFont(font)
        self.calculate_density_pushButton.setStyleSheet("background-color: rgb(0, 255, 127);")
        self.calculate_density_pushButton.setObjectName("calculate_density_pushButton")
        self.calculate_dynamic_viscocity_pushButton = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: self.calculate_dynamic_viscocity())
        self.calculate_dynamic_viscocity_pushButton.setGeometry(QtCore.QRect(590, 360, 300, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.calculate_dynamic_viscocity_pushButton.setFont(font)
        self.calculate_dynamic_viscocity_pushButton.setStyleSheet("background-color: rgb(0, 255, 127);")
        self.calculate_dynamic_viscocity_pushButton.setObjectName("calculate_dynamic_viscocity_pushButton")
        self.calculate_reynolds_number_pushButton = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: self.calculate_reynolds_number())
        self.calculate_reynolds_number_pushButton.setGeometry(QtCore.QRect(590, 420, 300, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.calculate_reynolds_number_pushButton.setFont(font)
        self.calculate_reynolds_number_pushButton.setStyleSheet("background-color: rgb(0, 255, 127);")
        self.calculate_reynolds_number_pushButton.setObjectName("calculate_reynolds_number_pushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1231, 21))
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
        self.altitude_label.setText(_translate("MainWindow", "Altitude (m)"))
        self.humidity_label.setText(_translate("MainWindow", "Humidity (%)"))
        self.barometric_pressure_label.setText(_translate("MainWindow", "Barometric Pressure (Pa)"))
        self.density_label.setText(_translate("MainWindow", "Density (kg/m^3)"))
        self.temperature_label.setText(_translate("MainWindow", "Temperature (K)"))
        self.dynamic_viscocity_label.setText(_translate("MainWindow", "Dynamic Viscocity (Pa·s)"))
        self.velocity_label.setText(_translate("MainWindow", "Velocity (m/s)"))
        self.chord_length_label.setText(_translate("MainWindow", "Chord Length (m)"))
        self.reynolds_number_label.setText(_translate("MainWindow", "Reynolds Number"))
        self.calculate_density_pushButton.setText(_translate("MainWindow", "Calculate Desnity"))
        self.calculate_dynamic_viscocity_pushButton.setText(_translate("MainWindow", "Calculate Dynamic Viscocity"))
        self.calculate_reynolds_number_pushButton.setText(_translate("MainWindow", "Calculate Reynolds Number"))

    def calculate_density(self):
        altitude = float(self.altitude_lineEdit.text())
        humidity = float(self.humidity_lineEdit.text())
        barometric_pressure = float(self.barometric_pressure_lineEdit.text())
        density = main_density(altitude, humidity, barometric_pressure)
        self.density_lineEdit.setText(str(density))

    def calculate_dynamic_viscocity(self):
        temperature = float(self.temperature_lineEdit.text())
        dynamic_viscocity = dynamic_viscosity(temperature)
        self.dynamic_viscocity_lineEdit.setText(str(dynamic_viscocity))

    def calculate_reynolds_number(self):
        density = float(self.density_lineEdit.text())
        velocity = float(self.velocity_lineEdit.text())
        characteristic_length = float(self.chord_length_lineEdit.text())
        dynamic_viscosity = float(self.dynamic_viscocity_lineEdit.text())
        reynolds_number = main_reynolds(density, velocity, characteristic_length, dynamic_viscosity)
        self.reynolds_number_lineEdit.setText(str(reynolds_number))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
