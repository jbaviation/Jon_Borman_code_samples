# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'setup_GUI.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_dialog(object):
    def setupUi(self, dialog):
        dialog.setObjectName("dialog")
        dialog.resize(545, 442)
        self.buttonBox = QtWidgets.QDialogButtonBox(dialog)
        self.buttonBox.setGeometry(QtCore.QRect(170, 370, 341, 32))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.buttonBox.setFont(font)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.groupBox = QtWidgets.QGroupBox(dialog)
        self.groupBox.setGeometry(QtCore.QRect(20, 20, 491, 161))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(20, 75, 471, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.tempChkBox = QtWidgets.QCheckBox(self.groupBox)
        self.tempChkBox.setGeometry(QtCore.QRect(50, 120, 441, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.tempChkBox.setFont(font)
        self.tempChkBox.setObjectName("tempChkBox")
        self.dpGenChkBox = QtWidgets.QCheckBox(self.groupBox)
        self.dpGenChkBox.setGeometry(QtCore.QRect(50, 100, 441, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.dpGenChkBox.setFont(font)
        self.dpGenChkBox.setObjectName("dpGenChkBox")
        self.label3 = QtWidgets.QLabel(self.groupBox)
        self.label3.setGeometry(QtCore.QRect(20, 38, 171, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label3.setFont(font)
        self.label3.setObjectName("label3")
        self.lineLC = QtWidgets.QLineEdit(self.groupBox)
        self.lineLC.setGeometry(QtCore.QRect(190, 37, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.lineLC.setFont(font)
        self.lineLC.setText("")
        self.lineLC.setPlaceholderText("")
        self.lineLC.setObjectName("lineLC")
        self.groupBox_2 = QtWidgets.QGroupBox(dialog)
        self.groupBox_2.setGeometry(QtCore.QRect(20, 210, 491, 121))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setObjectName("groupBox_2")
        self.pressChkBox = QtWidgets.QCheckBox(self.groupBox_2)
        self.pressChkBox.setGeometry(QtCore.QRect(50, 80, 181, 17))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.pressChkBox.setFont(font)
        self.pressChkBox.setObjectName("pressChkBox")
        self.label4 = QtWidgets.QLabel(self.groupBox_2)
        self.label4.setGeometry(QtCore.QRect(20, 37, 171, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label4.setFont(font)
        self.label4.setObjectName("label4")
        self.lineWVSS = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineWVSS.setGeometry(QtCore.QRect(190, 40, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.lineWVSS.setFont(font)
        self.lineWVSS.setText("")
        self.lineWVSS.setPlaceholderText("")
        self.lineWVSS.setClearButtonEnabled(False)
        self.lineWVSS.setObjectName("lineWVSS")

        self.retranslateUi(dialog)
        QtCore.QMetaObject.connectSlotsByName(dialog)

    def retranslateUi(self, dialog):
        _translate = QtCore.QCoreApplication.translate
        dialog.setWindowTitle(_translate("dialog", "Port Configuration"))
        self.groupBox.setTitle(_translate("dialog", "DataQ DI-145"))
        self.label_3.setText(_translate("dialog", "Select Which Devices Are Connected To DataQ DI-145:"))
        self.tempChkBox.setText(_translate("dialog", "Temperature (Ch 2)"))
        self.dpGenChkBox.setText(_translate("dialog", "Dew Point Generator (Ch 1)"))
        self.label3.setText(_translate("dialog", "USB COM port: "))
        self.groupBox_2.setTitle(_translate("dialog", "Water Vapor Monitor System"))
        self.pressChkBox.setText(_translate("dialog", "Use Pressure"))
        self.label4.setText(_translate("dialog", "RS232 COM port: "))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QDialog()
    ui = Ui_dialog()
    ui.setupUi(dialog)
    dialog.show()
    sys.exit(app.exec_())