'''Common methods that are not required to be class/instance methods.'''
from PyQt5 import QtCore, QtWidgets

# Non-class variable
def error_msg():
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Critical)
    msg.setWindowTitle('Error')
    return msg
