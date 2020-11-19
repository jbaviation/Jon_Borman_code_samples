# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'setConditions_GUI.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 273)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 220, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.setPressChkBox = QtWidgets.QCheckBox(Dialog)
        self.setPressChkBox.setGeometry(QtCore.QRect(30, 20, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.setPressChkBox.setFont(font)
        self.setPressChkBox.setChecked(True)
        self.setPressChkBox.setObjectName("setPressChkBox")
        self.setTempChkBox = QtWidgets.QCheckBox(Dialog)
        self.setTempChkBox.setGeometry(QtCore.QRect(30, 100, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.setTempChkBox.setFont(font)
        self.setTempChkBox.setChecked(True)
        self.setTempChkBox.setObjectName("setTempChkBox")
        self.pressUnitDD = QtWidgets.QComboBox(Dialog)
        self.pressUnitDD.setGeometry(QtCore.QRect(230, 50, 81, 31))
        self.pressUnitDD.setObjectName("pressUnitDD")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(50, 50, 51, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(50, 130, 51, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.tempUnitDD = QtWidgets.QComboBox(Dialog)
        self.tempUnitDD.setGeometry(QtCore.QRect(230, 130, 81, 31))
        self.tempUnitDD.setObjectName("tempUnitDD")
        self.pressLineEdit = QtWidgets.QLineEdit(Dialog)
        self.pressLineEdit.setGeometry(QtCore.QRect(102, 50, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pressLineEdit.setFont(font)
        self.pressLineEdit.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.pressLineEdit.setObjectName("pressLineEdit")
        self.tempLineEdit = QtWidgets.QLineEdit(Dialog)
        self.tempLineEdit.setGeometry(QtCore.QRect(100, 130, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.tempLineEdit.setFont(font)
        self.tempLineEdit.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.tempLineEdit.setObjectName("tempLineEdit")

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Set Conditions"))
        self.setPressChkBox.setText(_translate("Dialog", "Set Pressure"))
        self.setTempChkBox.setText(_translate("Dialog", "Set Temperature"))
        self.label.setText(_translate("Dialog", "Value:"))
        self.label_2.setText(_translate("Dialog", "Value:"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
