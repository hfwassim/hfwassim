import sys
from PyQt5 import *
from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import * 
from main import *

class MainDialogue(QtWidgets.QDialog):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        self.dialo = Ui_Dialog()
        self.lk = MainWindow()
        self.dialo.setupUi(self)

        self.lk.show()


app = QApplication(sys.argv)
win = MainDialogue()
win.show()

sys.exit(app.exec_())