# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_sectormean.ui'
#
# Created: Wed Oct 21 07:32:31 2015
#      by: PyQt4 UI code generator 4.10.4
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
        SectorMean.resize(330, 250)
        SectorMean.setMinimumSize(QtCore.QSize(330, 250))
        SectorMean.setMaximumSize(QtCore.QSize(330, 250))
        self.layoutWidget = QtGui.QWidget(SectorMean)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 311, 32))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.horizontalLayout_9 = QtGui.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_9.setMargin(0)
        self.horizontalLayout_9.setObjectName(_fromUtf8("horizontalLayout_9"))
        self.label_1 = QtGui.QLabel(self.layoutWidget)
        self.label_1.setMinimumSize(QtCore.QSize(0, 20))
        self.label_1.setObjectName(_fromUtf8("label_1"))
        self.horizontalLayout_9.addWidget(self.label_1)
        self.InPoint = QtGui.QComboBox(self.layoutWidget)
        self.InPoint.setMinimumSize(QtCore.QSize(210, 23))
        self.InPoint.setMaximumSize(QtCore.QSize(210, 23))
        self.InPoint.setObjectName(_fromUtf8("InPoint"))
        self.horizontalLayout_9.addWidget(self.InPoint)
        self.layoutWidget_2 = QtGui.QWidget(SectorMean)
        self.layoutWidget_2.setGeometry(QtCore.QRect(10, 42, 311, 32))
        self.layoutWidget_2.setObjectName(_fromUtf8("layoutWidget_2"))
        self.horizontalLayout_10 = QtGui.QHBoxLayout(self.layoutWidget_2)
        self.horizontalLayout_10.setMargin(0)
        self.horizontalLayout_10.setObjectName(_fromUtf8("horizontalLayout_10"))
        self.label_2 = QtGui.QLabel(self.layoutWidget_2)
        self.label_2.setMinimumSize(QtCore.QSize(0, 20))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_10.addWidget(self.label_2)
        self.InRast = QtGui.QComboBox(self.layoutWidget_2)
        self.InRast.setMinimumSize(QtCore.QSize(210, 23))
        self.InRast.setMaximumSize(QtCore.QSize(210, 23))
        self.InRast.setObjectName(_fromUtf8("InRast"))
        self.horizontalLayout_10.addWidget(self.InRast)
        self.buttonSaveAs = QtGui.QPushButton(SectorMean)
        self.buttonSaveAs.setGeometry(QtCore.QRect(188, 79, 135, 23))
        self.buttonSaveAs.setMinimumSize(QtCore.QSize(135, 23))
        self.buttonSaveAs.setMaximumSize(QtCore.QSize(135, 23))
        self.buttonSaveAs.setToolTip(_fromUtf8(""))
        self.buttonSaveAs.setObjectName(_fromUtf8("buttonSaveAs"))
        self.groupBox = QtGui.QGroupBox(SectorMean)
        self.groupBox.setGeometry(QtCore.QRect(8, 109, 315, 135))
        self.groupBox.setMinimumSize(QtCore.QSize(315, 135))
        self.groupBox.setMaximumSize(QtCore.QSize(315, 135))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.layoutWidget_4 = QtGui.QWidget(self.groupBox)
        self.layoutWidget_4.setGeometry(QtCore.QRect(10, 30, 291, 29))
        self.layoutWidget_4.setObjectName(_fromUtf8("layoutWidget_4"))
        self.horizontalLayout_11 = QtGui.QHBoxLayout(self.layoutWidget_4)
        self.horizontalLayout_11.setMargin(0)
        self.horizontalLayout_11.setObjectName(_fromUtf8("horizontalLayout_11"))
        self.cbxActive = QtGui.QCheckBox(self.layoutWidget_4)
        self.cbxActive.setMinimumSize(QtCore.QSize(0, 20))
        self.cbxActive.setToolTip(_fromUtf8(""))
        self.cbxActive.setObjectName(_fromUtf8("cbxActive"))
        self.horizontalLayout_11.addWidget(self.cbxActive)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_11.addItem(spacerItem)
        self.line_2 = QtGui.QFrame(self.layoutWidget_4)
        self.line_2.setFrameShape(QtGui.QFrame.VLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.horizontalLayout_11.addWidget(self.line_2)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_11.addItem(spacerItem1)
        self.label_11 = QtGui.QLabel(self.layoutWidget_4)
        self.label_11.setMinimumSize(QtCore.QSize(0, 20))
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.horizontalLayout_11.addWidget(self.label_11)
        self.bufferz0 = QtGui.QSpinBox(self.layoutWidget_4)
        self.bufferz0.setMinimumSize(QtCore.QSize(0, 23))
        self.bufferz0.setMaximumSize(QtCore.QSize(16777215, 23))
        self.bufferz0.setMinimum(0)
        self.bufferz0.setMaximum(10000)
        self.bufferz0.setSingleStep(100)
        self.bufferz0.setProperty("value", 1500)
        self.bufferz0.setObjectName(_fromUtf8("bufferz0"))
        self.horizontalLayout_11.addWidget(self.bufferz0)
        self.layoutWidget_3 = QtGui.QWidget(self.groupBox)
        self.layoutWidget_3.setGeometry(QtCore.QRect(10, 85, 291, 32))
        self.layoutWidget_3.setObjectName(_fromUtf8("layoutWidget_3"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.layoutWidget_3)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.outputXEdit = QtGui.QTextEdit(self.layoutWidget_3)
        self.outputXEdit.setMinimumSize(QtCore.QSize(90, 30))
        self.outputXEdit.setMaximumSize(QtCore.QSize(90, 30))
        self.outputXEdit.setObjectName(_fromUtf8("outputXEdit"))
        self.horizontalLayout_2.addWidget(self.outputXEdit)
        self.outputYEdit = QtGui.QTextEdit(self.layoutWidget_3)
        self.outputYEdit.setMinimumSize(QtCore.QSize(90, 30))
        self.outputYEdit.setMaximumSize(QtCore.QSize(90, 30))
        self.outputYEdit.setObjectName(_fromUtf8("outputYEdit"))
        self.horizontalLayout_2.addWidget(self.outputYEdit)
        self.outputMean = QtGui.QTextEdit(self.layoutWidget_3)
        self.outputMean.setMinimumSize(QtCore.QSize(90, 30))
        self.outputMean.setMaximumSize(QtCore.QSize(90, 30))
        self.outputMean.setObjectName(_fromUtf8("outputMean"))
        self.horizontalLayout_2.addWidget(self.outputMean)
        self.horizontalLayoutWidget = QtGui.QWidget(self.groupBox)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 70, 291, 17))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_3 = QtGui.QLabel(self.horizontalLayoutWidget)
        self.label_3.setMinimumSize(QtCore.QSize(90, 0))
        self.label_3.setMaximumSize(QtCore.QSize(90, 33))
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout.addWidget(self.label_3)
        self.label = QtGui.QLabel(self.horizontalLayoutWidget)
        self.label.setMinimumSize(QtCore.QSize(90, 0))
        self.label.setMaximumSize(QtCore.QSize(90, 33))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.label_4 = QtGui.QLabel(self.horizontalLayoutWidget)
        self.label_4.setMinimumSize(QtCore.QSize(90, 0))
        self.label_4.setMaximumSize(QtCore.QSize(90, 33))
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout.addWidget(self.label_4)
        self.progressBar = QtGui.QProgressBar(SectorMean)
        self.progressBar.setGeometry(QtCore.QRect(10, 80, 160, 21))
        self.progressBar.setMinimumSize(QtCore.QSize(160, 21))
        self.progressBar.setMaximumSize(QtCore.QSize(160, 21))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))

        self.retranslateUi(SectorMean)
        QtCore.QMetaObject.connectSlotsByName(SectorMean)

    def retranslateUi(self, SectorMean):
        SectorMean.setWindowTitle(_translate("SectorMean", "Sektormittelwerte", None))
        self.label_1.setText(_translate("SectorMean", "Standortdatei", None))
        self.label_2.setText(_translate("SectorMean", "Rauhigkeit (z0)", None))
        self.buttonSaveAs.setText(_translate("SectorMean", "Analyse speichern", None))
        self.groupBox.setTitle(_translate("SectorMean", "Interaktive Anzeige", None))
        self.cbxActive.setText(_translate("SectorMean", "Start/Stop", None))
        self.label_11.setText(_translate("SectorMean", "Radius (z0)", None))
        self.label_3.setText(_translate("SectorMean", "X-Wert", None))
        self.label.setText(_translate("SectorMean", "Y-Wert", None))
        self.label_4.setText(_translate("SectorMean", "Mittelwert (z0)", None))

