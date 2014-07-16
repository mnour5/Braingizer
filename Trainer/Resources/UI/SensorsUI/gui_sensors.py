# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Resources/UI/SensorsUI/gui_sensors.ui'
#
# Created: Wed Jul 16 11:20:14 2014
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

class Ui_SensorsWindow(object):
    def setupUi(self, SensorsWindow):
        SensorsWindow.setObjectName(_fromUtf8("SensorsWindow"))
        SensorsWindow.resize(541, 511)
        SensorsWindow.setMinimumSize(QtCore.QSize(541, 511))
        SensorsWindow.setMaximumSize(QtCore.QSize(541, 511))
        self.centralwidget = QtGui.QWidget(SensorsWindow)
        self.centralwidget.setStyleSheet(_fromUtf8(""))
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.label_9 = QtGui.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(0, 0, 541, 511))
        self.label_9.setStyleSheet(_fromUtf8(""))
        self.label_9.setText(_fromUtf8(""))
        self.label_9.setPixmap(QtGui.QPixmap(_fromUtf8("Resources/IMGs/SensorsUI_Back.png")))
        self.label_9.setObjectName(_fromUtf8("label_9"))
        SensorsWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(SensorsWindow)
        QtCore.QMetaObject.connectSlotsByName(SensorsWindow)

    def retranslateUi(self, SensorsWindow):
        SensorsWindow.setWindowTitle(_translate("SensorsWindow", "Braingizer Trainer - Sensors", None))

