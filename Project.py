
''' Mini-aplikacja kalendarz dla biegu
    1.Na poczatku prosi login i hasło ,jezeli nie masz konta, jest możliwość go stworzyć 
    (sprawdza dane lub dodaje nowego użytkownika do pliku)
    2.podczas podania dystansu i czasu oblicza szybkość i zapisuje do pliku.
    
     
'''
from os import name
import csv
import sys
from datetime import datetime
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication,QTableWidgetItem
from PyQt5.uic import loadUi

class Login(QDialog):
    def __init__(self):
        super(Login, self).__init__()
        loadUi("logowanie.ui", self)
        self.Login.clicked.connect(self.loginfunction)
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pushButton.clicked.connect(self.gotocreate)

    def loginfunction(self):
        name = self.lineEdit.text()
        password = self.lineEdit_2.text()
        #sprawdzic czy istnije czy nie 
        if self.check_user(name, password):
            QtWidgets.QMessageBox.information(self, "Success", "Successfully logged in!")
            self.calendarwindow()
        else:
            QtWidgets.QMessageBox.warning(self, "Error", "User not found or incorrect password.")

    
    def calendarwindow(self):
        calendaR=Calendar()
        widget.addWidget(calendaR)
        widget.setFixedWidth(1023)
        widget.setFixedHeight(631)
        widget.setCurrentIndex(widget.currentIndex() + 1)
    def gotocreate(self):
        createacc = CreateAcc()
        widget.addWidget(createacc)
        widget.setCurrentIndex(widget.currentIndex() + 1)
    def check_user(self, name, password):
        try:
            # Open the CSV file for reading
            with open('users.csv', 'r') as csvfile:
                 csvreader = csv.reader(csvfile)
        # Iterate over each row in the CSV
                 for row in csvreader:
                     if name == row[0]:
                        return password == row[1]

        except FileNotFoundError:
            return False
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

      

class CreateAcc(QDialog):
    def __init__(self):
        super(CreateAcc, self).__init__()
        loadUi("Create.acc.ui", self)
        self.Singup.clicked.connect(self.createaccfunction)
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_3.setEchoMode(QtWidgets.QLineEdit.Password)

    def createaccfunction(self):
        name = self.lineEdit.text()
        if self.lineEdit_2.text() == self.lineEdit_3.text():
            password = self.lineEdit_2.text()
              # Zapisujemy dane użytkownika do pliku
        with open('users.csv', 'a') as file:
                    writer = csv.writer(file)
                    writer.writerow([name, password])

       # print("Successfully created acc with name:", name, "and password:", password)
        QtWidgets.QMessageBox.information(self, "Success", "Successfully sing up!")
        login = Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class Calendar(QDialog):
    def __init__(self):
        super(Calendar, self).__init__()
        loadUi("Kalendarz.ui", self)
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.lineEdit_3.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.logout.clicked.connect(self.logOut)
        self.SaveButton.clicked.connect(self.saveData)  # Teraz metoda saveData jest w klasie
        self.calendar.selectionChanged.connect(self.calendarDateChanged)

    def logOut(self):
        QtWidgets.QMessageBox.information(self, " ", "Logging out...")
        QApplication.instance().quit()

    def saveData(self):
        selected_date = self.calendar.selectedDate()
        date_str = selected_date.toString("yyyy-MM-dd")
        distance = self.lineEdit_2.text()
        weight = 70  # Przykładowa waga

        # Sprawdź format czasu
        time_str = self.lineEdit_3.text()
        try:
            time_obj = datetime.strptime(time_str, "%H:%M")
            hours = time_obj.hour
            minutes = time_obj.minute
            total_hours = hours + minutes / 60

             # Oblicz szybkość
            if total_hours > 0: 
                 speed = float(distance) / total_hours  # km/h
            else:
                speed = 0

            # Oblicz spalone kalorie
            calories_burned = float(distance) * weight * 1.036
           
            with open('data.csv', 'a') as file:
                writer = csv.writer(file)
                writer.writerow([date_str, distance, f"{hours}:{minutes}", calories_burned,speed])

            QtWidgets.QMessageBox.information(self, " ", f"Data saved\nDate: {date_str}\nDistance: {distance} km\nTime: {hours}:{minutes}\nCalories Burned: {calories_burned:.2f}\nSpeed: {speed:.2f} km/h")
        except ValueError:
            QtWidgets.QMessageBox.warning(self, "Warning", "Invalid TIME format. Please use 'h:mm'.")

    def calendarDateChanged(self):
        QtWidgets.QMessageBox.information(self, " ", "Change data")


app = QApplication(sys.argv)
mainwindow = Login()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(490)
widget.setFixedHeight(600)
widget.show()
sys.exit(app.exec_())

