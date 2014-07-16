# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Resources/UI/DetectUI/gui_detect.ui'
#
# Created: Sat Jul 12 00:04:48 2014
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

class Ui_DetectWindow(object):
    def setupUi(self, DetectWindow):
        DetectWindow.setObjectName(_fromUtf8("DetectWindow"))
        DetectWindow.resize(810, 600)
        DetectWindow.setMinimumSize(QtCore.QSize(810, 600))
        self.centralwidget = QtGui.QWidget(DetectWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.untoggleIcon = QtGui.QLabel(self.centralwidget)
        self.untoggleIcon.setGeometry(QtCore.QRect(770, 10, 24, 24))
        self.untoggleIcon.setText(_fromUtf8(""))
        self.untoggleIcon.setPixmap(QtGui.QPixmap(_fromUtf8("Resources/IMGs/DetectUI_Untoggled.png")))
        self.untoggleIcon.setObjectName(_fromUtf8("untoggleIcon"))
        self.NoteFrame_3 = QtGui.QFrame(self.centralwidget)
        self.NoteFrame_3.setGeometry(QtCore.QRect(215, 430, 370, 110))
        self.NoteFrame_3.setFrameShape(QtGui.QFrame.NoFrame)
        self.NoteFrame_3.setFrameShadow(QtGui.QFrame.Raised)
        self.NoteFrame_3.setObjectName(_fromUtf8("NoteFrame_3"))
        self.Note3_Label = QtGui.QLabel(self.NoteFrame_3)
        self.Note3_Label.setGeometry(QtCore.QRect(0, 10, 370, 40))
        self.Note3_Label.setText(_fromUtf8("<html><head/><body><p align=\"center\"><span style=\" font-size:20pt;\">Right detected.</span></p><p align=\"center\"><span style=\" font-size:12pt;\">Wrong? Press escape, spacebar or hit this button:</span></p></body></html>"))
        self.Note3_Label.setObjectName(_fromUtf8("Note3_Label"))
        self.detalisParent_Frame = QtGui.QFrame(self.centralwidget)
        self.detalisParent_Frame.setGeometry(QtCore.QRect(10, 10, 790, 60))
        self.detalisParent_Frame.setAutoFillBackground(True)
        self.detalisParent_Frame.setFrameShape(QtGui.QFrame.NoFrame)
        self.detalisParent_Frame.setFrameShadow(QtGui.QFrame.Raised)
        self.detalisParent_Frame.setObjectName(_fromUtf8("detalisParent_Frame"))
        self.details_Line = QtGui.QFrame(self.detalisParent_Frame)
        self.details_Line.setGeometry(QtCore.QRect(0, 50, 790, 16))
        self.details_Line.setFrameShape(QtGui.QFrame.HLine)
        self.details_Line.setFrameShadow(QtGui.QFrame.Sunken)
        self.details_Line.setObjectName(_fromUtf8("details_Line"))
        self.toggleIcon = QtGui.QLabel(self.detalisParent_Frame)
        self.toggleIcon.setGeometry(QtCore.QRect(760, 0, 24, 24))
        self.toggleIcon.setText(_fromUtf8(""))
        self.toggleIcon.setPixmap(QtGui.QPixmap(_fromUtf8("Resources/IMGs/DetectUI_Toggled.png")))
        self.toggleIcon.setObjectName(_fromUtf8("toggleIcon"))
        self.detalisChild_Frame = QtGui.QFrame(self.detalisParent_Frame)
        self.detalisChild_Frame.setGeometry(QtCore.QRect(0, 0, 560, 50))
        self.detalisChild_Frame.setAutoFillBackground(True)
        self.detalisChild_Frame.setFrameShape(QtGui.QFrame.NoFrame)
        self.detalisChild_Frame.setFrameShadow(QtGui.QFrame.Raised)
        self.detalisChild_Frame.setObjectName(_fromUtf8("detalisChild_Frame"))
        self.label_9 = QtGui.QLabel(self.detalisChild_Frame)
        self.label_9.setGeometry(QtCore.QRect(0, 0, 111, 17))
        self.label_9.setStyleSheet(_fromUtf8("font: bold;"))
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.Name_Label = QtGui.QLabel(self.detalisChild_Frame)
        self.Name_Label.setGeometry(QtCore.QRect(0, 20, 161, 17))
        self.Name_Label.setObjectName(_fromUtf8("Name_Label"))
        self.ClassifierName_Label = QtGui.QLabel(self.detalisChild_Frame)
        self.ClassifierName_Label.setGeometry(QtCore.QRect(200, 20, 160, 17))
        self.ClassifierName_Label.setObjectName(_fromUtf8("ClassifierName_Label"))
        self.label_13 = QtGui.QLabel(self.detalisChild_Frame)
        self.label_13.setGeometry(QtCore.QRect(200, 0, 120, 17))
        self.label_13.setStyleSheet(_fromUtf8("font: bold;"))
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.AvgTime_Label = QtGui.QLabel(self.detalisChild_Frame)
        self.AvgTime_Label.setGeometry(QtCore.QRect(370, 20, 140, 17))
        self.AvgTime_Label.setObjectName(_fromUtf8("AvgTime_Label"))
        self.label_14 = QtGui.QLabel(self.detalisChild_Frame)
        self.label_14.setGeometry(QtCore.QRect(370, 0, 150, 17))
        self.label_14.setStyleSheet(_fromUtf8("font: bold;"))
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.Arrows_Frame_Normal = QtGui.QFrame(self.centralwidget)
        self.Arrows_Frame_Normal.setGeometry(QtCore.QRect(220, 90, 370, 110))
        self.Arrows_Frame_Normal.setFrameShape(QtGui.QFrame.NoFrame)
        self.Arrows_Frame_Normal.setFrameShadow(QtGui.QFrame.Raised)
        self.Arrows_Frame_Normal.setObjectName(_fromUtf8("Arrows_Frame_Normal"))
        self.RightArrow_Normal = QtGui.QLabel(self.Arrows_Frame_Normal)
        self.RightArrow_Normal.setGeometry(QtCore.QRect(215, 0, 155, 110))
        self.RightArrow_Normal.setText(_fromUtf8(""))
        self.RightArrow_Normal.setPixmap(QtGui.QPixmap(_fromUtf8("Resources/IMGs/DetectUI_RightArrow_Normal_Grey.png")))
        self.RightArrow_Normal.setObjectName(_fromUtf8("RightArrow_Normal"))
        self.LeftArrow_Normal = QtGui.QLabel(self.Arrows_Frame_Normal)
        self.LeftArrow_Normal.setGeometry(QtCore.QRect(0, 0, 155, 110))
        self.LeftArrow_Normal.setText(_fromUtf8(""))
        self.LeftArrow_Normal.setPixmap(QtGui.QPixmap(_fromUtf8("Resources/IMGs/DetectUI_LeftArrow_Normal_Grey.png")))
        self.LeftArrow_Normal.setObjectName(_fromUtf8("LeftArrow_Normal"))
        self.Arrows_Frame = QtGui.QFrame(self.centralwidget)
        self.Arrows_Frame.setGeometry(QtCore.QRect(130, 220, 560, 180))
        self.Arrows_Frame.setFrameShape(QtGui.QFrame.NoFrame)
        self.Arrows_Frame.setFrameShadow(QtGui.QFrame.Raised)
        self.Arrows_Frame.setObjectName(_fromUtf8("Arrows_Frame"))
        self.RightArrow = QtGui.QLabel(self.Arrows_Frame)
        self.RightArrow.setGeometry(QtCore.QRect(369, 52, 188, 41))
        self.RightArrow.setText(_fromUtf8(""))
        self.RightArrow.setPixmap(QtGui.QPixmap(_fromUtf8("Resources/IMGs/DetectUI_RightArrow_Grey.png")))
        self.RightArrow.setObjectName(_fromUtf8("RightArrow"))
        self.LeftArrow = QtGui.QLabel(self.Arrows_Frame)
        self.LeftArrow.setGeometry(QtCore.QRect(2, 57, 188, 41))
        self.LeftArrow.setText(_fromUtf8(""))
        self.LeftArrow.setPixmap(QtGui.QPixmap(_fromUtf8("Resources/IMGs/DetectUI_LeftArrow_Grey.png")))
        self.LeftArrow.setObjectName(_fromUtf8("LeftArrow"))
        self.BwdArrow = QtGui.QLabel(self.Arrows_Frame)
        self.BwdArrow.setGeometry(QtCore.QRect(200, 100, 156, 80))
        self.BwdArrow.setText(_fromUtf8(""))
        self.BwdArrow.setPixmap(QtGui.QPixmap(_fromUtf8("Resources/IMGs/DetectUI_BackArrow_Grey.png")))
        self.BwdArrow.setObjectName(_fromUtf8("BwdArrow"))
        self.FwdArrow = QtGui.QLabel(self.Arrows_Frame)
        self.FwdArrow.setGeometry(QtCore.QRect(225, 6, 112, 44))
        self.FwdArrow.setText(_fromUtf8(""))
        self.FwdArrow.setPixmap(QtGui.QPixmap(_fromUtf8("Resources/IMGs/DetectUI_FWDArrow_Grey.png")))
        self.FwdArrow.setObjectName(_fromUtf8("FwdArrow"))
        self.StopCircle = QtGui.QLabel(self.Arrows_Frame)
        self.StopCircle.setGeometry(QtCore.QRect(234, 59, 85, 33))
        self.StopCircle.setText(_fromUtf8(""))
        self.StopCircle.setPixmap(QtGui.QPixmap(_fromUtf8("Resources/IMGs/DetectUI_Stop_Grey.png")))
        self.StopCircle.setObjectName(_fromUtf8("StopCircle"))
        DetectWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(DetectWindow)
        QtCore.QMetaObject.connectSlotsByName(DetectWindow)

    def retranslateUi(self, DetectWindow):
        DetectWindow.setWindowTitle(_translate("DetectWindow", "Braingizer Detector - Detection Session", None))
        self.label_9.setText(_translate("DetectWindow", "<html><head/><body><p>Name</p></body></html>", None))
        self.Name_Label.setText(_translate("DetectWindow", "Mohamed Nour El-Din", None))
        self.ClassifierName_Label.setText(_translate("DetectWindow", "<html><head/><body><p>Fisher</p></body></html>", None))
        self.label_13.setText(_translate("DetectWindow", "<html><head/><body><p>Classifier Name</p></body></html>", None))
        self.AvgTime_Label.setText(_translate("DetectWindow", "<html><head/><body><p>0.00 sec</p></body></html>", None))
        self.label_14.setText(_translate("DetectWindow", "<html><head/><body><p>Avg. Detection Time</p></body></html>", None))

