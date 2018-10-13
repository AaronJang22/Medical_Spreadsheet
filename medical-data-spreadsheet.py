import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PyQt5 import uic

class Member():
    def __init__(self):
        pass

    def InitMember(self):
        with open("save.txt") as f:
            f.seek(0)
            first_char = f.read(1)
            if not first_char:
                self.name = []
                self.no = []
                self.cm = []
                self.age = []
                self.sex = []
                self.count = 0
            else:
                self.FileLoad()

    def FileLoad(self):
        f = open("save.txt", "r")

        self.name = f.readline().split()
        self.no = f.readline().split()
        self.cm = f.readline().split()
        self.age = f.readline().split()
        self.sex = f.readline().split()
        self.count = int(f.readline())

        f.close()

    def CreateMember(self, name, no, cm, age, sex):
        self.name.append(name)
        self.no.append(no)
        self.cm.append(cm)
        self.age.append(age)
        self.sex.append(sex)
        self.count+=1

        self.FileSave()

    def FileSave(self):
        f = open("save.txt", 'w+')

        f.write('\t'.join(self.name)+'\n')
        f.write('\t'.join(self.no)+'\n')
        f.write('\t'.join(self.cm)+'\n')
        f.write('\t'.join(self.age)+'\n')
        f.write('\t'.join(self.sex)+'\n')
        f.write(str(self.count))

        f.close()

    def DeleteMember(self, text):
        print('DeleteMember')

        for i in range(0,self.count):
            if int(text) == i:
                del self.name[i]
                del self.no[i]
                del self.cm[i]
                del self.age[i]
                del self.sex[i]
                self.count -= 1

                self.FileSave()

class imageWindow(QMainWindow):
    def __init__(self, mem):
        super().__init__()

        self.imageUI = uic.loadUi("imageWindow.ui", self)
        self.imageUI.show()

        self.mem = mem

        self.number = 1
        self.name = "image_1.jpg"

        self.initUI()

    def initUI(self):
        self.imageShow(self.name)

        self.imageUI.pushButton.clicked.connect(self.before)
        self.imageUI.pushButton_2.clicked.connect(self.after)

    def imageShow(self, name):
        self.label = QLabel()

        self.label.setPixmap(QPixmap(name))
        self.label.show()

    def before(self):
        if(1 < self.number):
            self.number -= 1

        print(self.number, self.mem.count)

        self.imageShow("image_" + str(self.number) + ".jpg")

    def after(self):
        if self.number < self.mem.count:
            self.number += 1

        print(self.number, self.mem.count)

        self.imageShow("image_" + str(self.number) + ".jpg")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.mem = Member()
        self.mem.InitMember()

        self.MainUI = uic.loadUi("MainWindow.ui", self)
        self.MainUI.show()

        self.initUI()

    def initUI(self):
        self.showAllButton()
        self.MainUI.pushButton.clicked.connect(self.search1Button)
        self.MainUI.pushButton_2.clicked.connect(self.showAllButton)
        #self.MainUI.pushButton_3.clicked.connect(self.search2Button)
        self.MainUI.pushButton_4.clicked.connect(self.signupButton)
        self.MainUI.pushButton_5.clicked.connect(self.inform)
        self.MainUI.pushButton_6.clicked.connect(self.deleteButton)

    def inform(self):
        image = imageWindow(self.mem)

    def search1Button(self):
        self.MainUI.tableWidget.clearContents()

        self.same = 0
        for i in range(0,self.mem.count):
            if self.mem.name[i] == self.MainUI.lineEdit.text() or self.mem.no[i] == self.MainUI.lineEdit_2.text():
                self.MainUI.tableWidget.setItem(self.same, 0, QTableWidgetItem(self.mem.name[i]))
                self.MainUI.tableWidget.setItem(self.same, 1, QTableWidgetItem(self.mem.no[i]))
                self.MainUI.tableWidget.setItem(self.same, 2, QTableWidgetItem(self.mem.cm[i]))
                self.MainUI.tableWidget.setItem(self.same, 3, QTableWidgetItem(self.mem.age[i]))
                self.MainUI.tableWidget.setItem(self.same, 4, QTableWidgetItem(self.mem.sex[i]))

                self.same += 1

    def showAllButton(self):
        for i in range(0, self.mem.count):
            self.MainUI.tableWidget.setItem(i, 0, QTableWidgetItem(self.mem.name[i]))
            self.MainUI.tableWidget.setItem(i, 1, QTableWidgetItem(self.mem.no[i]))
            self.MainUI.tableWidget.setItem(i, 2, QTableWidgetItem(self.mem.cm[i]))
            self.MainUI.tableWidget.setItem(i, 3, QTableWidgetItem(self.mem.age[i]))
            self.MainUI.tableWidget.setItem(i, 4, QTableWidgetItem(self.mem.sex[i]))

    def signupButton(self):
        sign = SignupWindow(self.mem)
        self.showAllButton()


    def deleteButton(self):
        text, okPressed = QInputDialog.getText(self, "회원 삭제","삭제할 회원번호를 입력하세요:", QLineEdit.Normal, "")

        if okPressed == True:
            text = str(int(text) - 1)
            self.mem.DeleteMember(text)

        self.showAllButton()

class SignupWindow(QMainWindow):
    def __init__(self, mem):
        super().__init__()

        self.SignupUi = uic.loadUi("SignupWindow.ui", self)
        self.SignupUi.show()

        self.mem = mem

        self.initUI()

    def initUI(self):
        self.SignupUi.pushButton.clicked.connect(self.signup)
        self.SignupUi.pushButton_2.clicked.connect(self.file_upload)

    def file_upload(self):
        pass


    def signup(self):
        if (self.SignupUi.radioButton.isChecked()):
            self.sex = "M"
        else:
            self.sex = "F"

        self.mem.CreateMember(self.SignupUi.lineEdit.text(), self.SignupUi.lineEdit_2.text(), self.SignupUi.lineEdit_3.text(), self.SignupUi.lineEdit_4.text(), self.sex)

        self.SignupUi.hide()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    app.exec_()

main()