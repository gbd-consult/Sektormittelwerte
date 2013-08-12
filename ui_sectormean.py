# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_sectormean.ui'
#
# Created by: PyQt4 UI code generator 4.9.6
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

class Ui_SectorMean(object):
    def setupUi(self, SectorMean):
        SectorMean.setObjectName(_fromUtf8("SectorMean"))
        SectorMean.resize(330, 135)
        SectorMean.setMinimumSize(QtCore.QSize(330, 135))
        SectorMean.setMaximumSize(QtCore.QSize(330, 135))
        self.buttonBox = QtGui.QDialogButtonBox(SectorMean)
        self.buttonBox.setGeometry(QtCore.QRect(120, 100, 201, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.layoutWidget = QtGui.QWidget(SectorMean)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 315, 32))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.horizontalLayout_9 = QtGui.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_9.setMargin(0)
        self.horizontalLayout_9.setObjectName(_fromUtf8("horizontalLayout_9"))
        self.label_1 = QtGui.QLabel(self.layoutWidget)
        self.label_1.setMinimumSize(QtCore.QSize(0, 20))
        self.label_1.setObjectName(_fromUtf8("label_1"))
        self.horizontalLayout_9.addWidget(self.label_1)
        self.InPoint = QtGui.QComboBox(self.layoutWidget)
        self.InPoint.setMinimumSize(QtCore.QSize(220, 23))
        self.InPoint.setMaximumSize(QtCore.QSize(220, 23))
        self.InPoint.setObjectName(_fromUtf8("InPoint"))
        self.horizontalLayout_9.addWidget(self.InPoint)
        self.layoutWidget_2 = QtGui.QWidget(SectorMean)
        self.layoutWidget_2.setGeometry(QtCore.QRect(10, 50, 315, 32))
        self.layoutWidget_2.setObjectName(_fromUtf8("layoutWidget_2"))
        self.horizontalLayout_10 = QtGui.QHBoxLayout(self.layoutWidget_2)
        self.horizontalLayout_10.setMargin(0)
        self.horizontalLayout_10.setObjectName(_fromUtf8("horizontalLayout_10"))
        self.label_2 = QtGui.QLabel(self.layoutWidget_2)
        self.label_2.setMinimumSize(QtCore.QSize(0, 20))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_10.addWidget(self.label_2)
        self.InRast = QtGui.QComboBox(self.layoutWidget_2)
        self.InRast.setMinimumSize(QtCore.QSize(220, 23))
        self.InRast.setMaximumSize(QtCore.QSize(220, 23))
        self.InRast.setObjectName(_fromUtf8("InRast"))
        self.horizontalLayout_10.addWidget(self.InRast)
        self.line = QtGui.QFrame(SectorMean)
        self.line.setGeometry(QtCore.QRect(20, 90, 281, 10))
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))

        self.retranslateUi(SectorMean)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), SectorMean.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), SectorMean.reject)
        QtCore.QMetaObject.connectSlotsByName(SectorMean)

    def retranslateUi(self, SectorMean):
        SectorMean.setWindowTitle(_translate("SectorMean", "SectorMean", None))
        self.label_1.setText(_translate("SectorMean", "Standorte", None))
        self.label_2.setText(_translate("SectorMean", "Rasterlayer", None))

