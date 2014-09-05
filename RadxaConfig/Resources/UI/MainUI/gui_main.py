# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Resources/UI/MainUI/gui_main.ui'
#
# Created: Thu Sep  4 01:07:18 2014
#      by: PyQt4 UI code generator 4.10
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(437, 510)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.configButton = QtGui.QPushButton(self.centralwidget)
        self.configButton.setGeometry(QtCore.QRect(140, 460, 130, 27))
        self.configButton.setObjectName(_fromUtf8("configButton"))
        self.TimingOptionsGroup = QtGui.QGroupBox(self.centralwidget)
        self.TimingOptionsGroup.setGeometry(QtCore.QRect(30, 300, 370, 140))
        self.TimingOptionsGroup.setObjectName(_fromUtf8("TimingOptionsGroup"))
        self.RecordingTime_LineEdit = QtGui.QLineEdit(self.TimingOptionsGroup)
        self.RecordingTime_LineEdit.setGeometry(QtCore.QRect(20, 100, 110, 27))
        self.RecordingTime_LineEdit.setObjectName(_fromUtf8("RecordingTime_LineEdit"))
        self.label_18 = QtGui.QLabel(self.TimingOptionsGroup)
        self.label_18.setGeometry(QtCore.QRect(140, 100, 40, 17))
        self.label_18.setStyleSheet(_fromUtf8("font: bold;"))
        self.label_18.setObjectName(_fromUtf8("label_18"))
        self.label_16 = QtGui.QLabel(self.TimingOptionsGroup)
        self.label_16.setGeometry(QtCore.QRect(20, 80, 120, 17))
        self.label_16.setStyleSheet(_fromUtf8("font: bold;"))
        self.label_16.setObjectName(_fromUtf8("label_16"))
        self.Classifiers_ComboBox = QtGui.QComboBox(self.TimingOptionsGroup)
        self.Classifiers_ComboBox.setGeometry(QtCore.QRect(20, 50, 345, 27))
        self.Classifiers_ComboBox.setObjectName(_fromUtf8("Classifiers_ComboBox"))
        self.label_9 = QtGui.QLabel(self.TimingOptionsGroup)
        self.label_9.setGeometry(QtCore.QRect(20, 30, 131, 17))
        self.label_9.setStyleSheet(_fromUtf8("font: bold;"))
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.TrainingFile_Group = QtGui.QGroupBox(self.centralwidget)
        self.TrainingFile_Group.setGeometry(QtCore.QRect(30, 110, 380, 160))
        self.TrainingFile_Group.setObjectName(_fromUtf8("TrainingFile_Group"))
        self.TrainingFile_ComboBox = QtGui.QComboBox(self.TrainingFile_Group)
        self.TrainingFile_ComboBox.setGeometry(QtCore.QRect(20, 130, 345, 27))
        self.TrainingFile_ComboBox.setObjectName(_fromUtf8("TrainingFile_ComboBox"))
        self.Sessions_RadioButton = QtGui.QRadioButton(self.TrainingFile_Group)
        self.Sessions_RadioButton.setGeometry(QtCore.QRect(200, 50, 130, 22))
        self.Sessions_RadioButton.setObjectName(_fromUtf8("Sessions_RadioButton"))
        self.label_15 = QtGui.QLabel(self.TrainingFile_Group)
        self.label_15.setGeometry(QtCore.QRect(20, 30, 170, 17))
        self.label_15.setStyleSheet(_fromUtf8("font: bold;"))
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.Sessions_ComboBox = QtGui.QComboBox(self.TrainingFile_Group)
        self.Sessions_ComboBox.setEnabled(False)
        self.Sessions_ComboBox.setGeometry(QtCore.QRect(200, 70, 164, 27))
        self.Sessions_ComboBox.setObjectName(_fromUtf8("Sessions_ComboBox"))
        self.Profile_RadioButton = QtGui.QRadioButton(self.TrainingFile_Group)
        self.Profile_RadioButton.setGeometry(QtCore.QRect(20, 50, 121, 22))
        self.Profile_RadioButton.setChecked(False)
        self.Profile_RadioButton.setObjectName(_fromUtf8("Profile_RadioButton"))
        self.Profile_ComboBox = QtGui.QComboBox(self.TrainingFile_Group)
        self.Profile_ComboBox.setEnabled(False)
        self.Profile_ComboBox.setGeometry(QtCore.QRect(20, 70, 170, 27))
        self.Profile_ComboBox.setObjectName(_fromUtf8("Profile_ComboBox"))
        self.label_17 = QtGui.QLabel(self.TrainingFile_Group)
        self.label_17.setGeometry(QtCore.QRect(20, 110, 131, 17))
        self.label_17.setStyleSheet(_fromUtf8("font: bold;"))
        self.label_17.setObjectName(_fromUtf8("label_17"))
        self.TimingOptionsGroup_2 = QtGui.QGroupBox(self.centralwidget)
        self.TimingOptionsGroup_2.setGeometry(QtCore.QRect(30, 20, 370, 70))
        self.TimingOptionsGroup_2.setObjectName(_fromUtf8("TimingOptionsGroup_2"))
        self.shutdownButton = QtGui.QPushButton(self.TimingOptionsGroup_2)
        self.shutdownButton.setGeometry(QtCore.QRect(200, 30, 160, 27))
        self.shutdownButton.setObjectName(_fromUtf8("shutdownButton"))
        self.rebootButton = QtGui.QPushButton(self.TimingOptionsGroup_2)
        self.rebootButton.setGeometry(QtCore.QRect(20, 30, 170, 27))
        self.rebootButton.setObjectName(_fromUtf8("rebootButton"))
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.Classifiers_ComboBox, self.configButton)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Radxa Configure", None))
        self.configButton.setText(_translate("MainWindow", "Configure Radxa", None))
        self.TimingOptionsGroup.setTitle(_translate("MainWindow", "Detection Options", None))
        self.RecordingTime_LineEdit.setText(_translate("MainWindow", "2", None))
        self.label_18.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" vertical-align:sub;\">seconds</span></p></body></html>", None))
        self.label_16.setText(_translate("MainWindow", "<html><head/><body><p>Recording Time</p></body></html>", None))
        self.label_9.setText(_translate("MainWindow", "<html><head/><body><p>Classifier Script</p></body></html>", None))
        self.TrainingFile_Group.setTitle(_translate("MainWindow", "Training File", None))
        self.Sessions_RadioButton.setText(_translate("MainWindow", "Session Name", None))
        self.label_15.setText(_translate("MainWindow", "<html><head/><body><p>Select by</p></body></html>", None))
        self.Profile_RadioButton.setText(_translate("MainWindow", "Profile Name", None))
        self.label_17.setText(_translate("MainWindow", "<html><head/><body><p>Training File</p></body></html>", None))
        self.TimingOptionsGroup_2.setTitle(_translate("MainWindow", "Power Options", None))
        self.shutdownButton.setText(_translate("MainWindow", "Shutdown", None))
        self.rebootButton.setText(_translate("MainWindow", "Reboot", None))

