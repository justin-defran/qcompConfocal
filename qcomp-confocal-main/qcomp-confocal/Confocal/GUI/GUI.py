# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUI.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_mwConfocal1(object):
    def setupUi(self, mwConfocal):
        mwConfocal.setObjectName("mwConfocal")
        mwConfocal.resize(1129, 722)
        self.centralwidget = QtWidgets.QWidget(mwConfocal)
        self.centralwidget.setObjectName("centralwidget")
        self.wEssence = QtWidgets.QWidget(self.centralwidget)
        self.wEssence.setGeometry(QtCore.QRect(0, 0, 1441, 761))
        self.wEssence.setObjectName("wEssence")
        self.wToolbar = QtWidgets.QWidget(self.wEssence)
        self.wToolbar.setGeometry(QtCore.QRect(50, 610, 371, 31))
        self.wToolbar.setObjectName("wToolbar")
        self.gbScan = QtWidgets.QGroupBox(self.wEssence)
        self.gbScan.setGeometry(QtCore.QRect(30, 80, 531, 181))
        self.gbScan.setObjectName("gbScan")
        self.gbX = QtWidgets.QGroupBox(self.gbScan)
        self.gbX.setGeometry(QtCore.QRect(10, 20, 161, 111))
        self.gbX.setObjectName("gbX")
        self.txtStepX = QtWidgets.QLineEdit(self.gbX)
        self.txtStepX.setGeometry(QtCore.QRect(60, 80, 91, 20))
        self.txtStepX.setObjectName("txtStepX")
        self.label = QtWidgets.QLabel(self.gbX)
        self.label.setGeometry(QtCore.QRect(10, 20, 46, 13))
        self.label.setObjectName("label")
        self.txtStartX = QtWidgets.QLineEdit(self.gbX)
        self.txtStartX.setGeometry(QtCore.QRect(60, 20, 91, 20))
        self.txtStartX.setObjectName("txtStartX")
        self.label_4 = QtWidgets.QLabel(self.gbX)
        self.label_4.setGeometry(QtCore.QRect(10, 80, 46, 13))
        self.label_4.setObjectName("label_4")
        self.label_3 = QtWidgets.QLabel(self.gbX)
        self.label_3.setGeometry(QtCore.QRect(10, 50, 46, 13))
        self.label_3.setObjectName("label_3")
        self.txtEndX = QtWidgets.QLineEdit(self.gbX)
        self.txtEndX.setGeometry(QtCore.QRect(60, 50, 91, 20))
        self.txtEndX.setObjectName("txtEndX")
        self.gbY = QtWidgets.QGroupBox(self.gbScan)
        self.gbY.setGeometry(QtCore.QRect(180, 20, 161, 111))
        self.gbY.setObjectName("gbY")
        self.txtStepY = QtWidgets.QLineEdit(self.gbY)
        self.txtStepY.setGeometry(QtCore.QRect(60, 80, 91, 20))
        self.txtStepY.setObjectName("txtStepY")
        self.label_5 = QtWidgets.QLabel(self.gbY)
        self.label_5.setGeometry(QtCore.QRect(10, 20, 46, 13))
        self.label_5.setObjectName("label_5")
        self.txtStartY = QtWidgets.QLineEdit(self.gbY)
        self.txtStartY.setGeometry(QtCore.QRect(60, 20, 91, 20))
        self.txtStartY.setObjectName("txtStartY")
        self.label_6 = QtWidgets.QLabel(self.gbY)
        self.label_6.setGeometry(QtCore.QRect(10, 80, 46, 13))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.gbY)
        self.label_7.setGeometry(QtCore.QRect(10, 50, 46, 13))
        self.label_7.setObjectName("label_7")
        self.txtEndY = QtWidgets.QLineEdit(self.gbY)
        self.txtEndY.setGeometry(QtCore.QRect(60, 50, 91, 20))
        self.txtEndY.setObjectName("txtEndY")
        self.pbStart = QtWidgets.QPushButton(self.gbScan)
        self.pbStart.setEnabled(False)
        self.pbStart.setGeometry(QtCore.QRect(350, 140, 75, 23))
        self.pbStart.setObjectName("pbStart")
        self.pbStop = QtWidgets.QPushButton(self.gbScan)
        self.pbStop.setEnabled(False)
        self.pbStop.setGeometry(QtCore.QRect(430, 140, 75, 23))
        self.pbStop.setObjectName("pbStop")
        self.gbSpeed = QtWidgets.QGroupBox(self.gbScan)
        self.gbSpeed.setGeometry(QtCore.QRect(10, 130, 331, 41))
        self.gbSpeed.setObjectName("gbSpeed")
        self.label_16 = QtWidgets.QLabel(self.gbSpeed)
        self.label_16.setGeometry(QtCore.QRect(70, 10, 131, 20))
        self.label_16.setObjectName("label_16")
        self.cbFreq = QtWidgets.QComboBox(self.gbSpeed)
        self.cbFreq.setGeometry(QtCore.QRect(200, 10, 73, 22))
        self.cbFreq.setObjectName("cbFreq")
        self.cbFreq.addItem("")
        self.cbFreq.addItem("")
        self.cbFreq.addItem("")
        self.cbFreq.addItem("")
        self.cbFreq.addItem("")
        self.cbFreq.addItem("")
        self.cbFreq.addItem("")
        self.pbCenter = QtWidgets.QPushButton(self.gbScan)
        self.pbCenter.setGeometry(QtCore.QRect(390, 70, 91, 23))
        self.pbCenter.setObjectName("pbCenter")
        self.pbFullScale = QtWidgets.QPushButton(self.gbScan)
        self.pbFullScale.setGeometry(QtCore.QRect(390, 30, 91, 23))
        self.pbFullScale.setObjectName("pbFullScale")
        self.label_2 = QtWidgets.QLabel(self.gbScan)
        self.label_2.setGeometry(QtCore.QRect(380, 100, 53, 16))
        self.label_2.setObjectName("label_2")
        self.txtRange = QtWidgets.QLineEdit(self.gbScan)
        self.txtRange.setGeometry(QtCore.QRect(420, 100, 71, 22))
        self.txtRange.setObjectName("txtRange")
        self.gbCounts = QtWidgets.QGroupBox(self.wEssence)
        self.gbCounts.setGeometry(QtCore.QRect(580, 260, 531, 401))
        self.gbCounts.setObjectName("gbCounts")
        self.pbCount = QtWidgets.QPushButton(self.gbCounts)
        self.pbCount.setEnabled(False)
        self.pbCount.setGeometry(QtCore.QRect(400, 40, 75, 23))
        self.pbCount.setObjectName("pbCount")
        self.pbMax = QtWidgets.QPushButton(self.gbCounts)
        self.pbMax.setEnabled(False)
        self.pbMax.setGeometry(QtCore.QRect(400, 120, 75, 23))
        self.pbMax.setObjectName("pbMax")
        self.cbCountFreq = QtWidgets.QComboBox(self.gbCounts)
        self.cbCountFreq.setEnabled(False)
        self.cbCountFreq.setGeometry(QtCore.QRect(400, 80, 73, 22))
        self.cbCountFreq.setObjectName("cbCountFreq")
        self.cbCountFreq.addItem("")
        self.cbCountFreq.addItem("")
        self.cbCountFreq.addItem("")
        self.cbCountFreq.addItem("")
        self.label_15 = QtWidgets.QLabel(self.gbCounts)
        self.label_15.setGeometry(QtCore.QRect(480, 80, 31, 16))
        self.label_15.setObjectName("label_15")
        self.lcdNumber = QtWidgets.QLCDNumber(self.gbCounts)
        self.lcdNumber.setGeometry(QtCore.QRect(10, 30, 381, 101))
        self.lcdNumber.setNumDigits(8)
        self.lcdNumber.setObjectName("lcdNumber")
        self.curvewidget = CurveWidget(self.gbCounts)
        self.curvewidget.setGeometry(QtCore.QRect(10, 150, 501, 231))
        self.curvewidget.setOrientation(QtCore.Qt.Horizontal)
        self.curvewidget.setObjectName("curvewidget")
        self.vsMax = QtWidgets.QSlider(self.wEssence)
        self.vsMax.setGeometry(QtCore.QRect(540, 280, 19, 321))
        self.vsMax.setProperty("value", 99)
        self.vsMax.setOrientation(QtCore.Qt.Vertical)
        self.vsMax.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.vsMax.setObjectName("vsMax")
        self.pbSlide = QtWidgets.QPushButton(self.wEssence)
        self.pbSlide.setEnabled(False)
        self.pbSlide.setGeometry(QtCore.QRect(530, 610, 41, 23))
        self.pbSlide.setObjectName("pbSlide")
        self.gbCursor = QtWidgets.QGroupBox(self.wEssence)
        self.gbCursor.setGeometry(QtCore.QRect(580, 10, 531, 151))
        self.gbCursor.setObjectName("gbCursor")
        self.gbX_2 = QtWidgets.QGroupBox(self.gbCursor)
        self.gbX_2.setGeometry(QtCore.QRect(50, 20, 161, 111))
        self.gbX_2.setObjectName("gbX_2")
        self.label_10 = QtWidgets.QLabel(self.gbX_2)
        self.label_10.setGeometry(QtCore.QRect(10, 20, 46, 13))
        self.label_10.setObjectName("label_10")
        self.txtXcom = QtWidgets.QLineEdit(self.gbX_2)
        self.txtXcom.setGeometry(QtCore.QRect(40, 20, 111, 20))
        self.txtXcom.setObjectName("txtXcom")
        self.label_13 = QtWidgets.QLabel(self.gbX_2)
        self.label_13.setGeometry(QtCore.QRect(10, 50, 46, 13))
        self.label_13.setObjectName("label_13")
        self.txtYcom = QtWidgets.QLineEdit(self.gbX_2)
        self.txtYcom.setGeometry(QtCore.QRect(40, 50, 111, 20))
        self.txtYcom.setObjectName("txtYcom")
        self.label_8 = QtWidgets.QLabel(self.gbX_2)
        self.label_8.setGeometry(QtCore.QRect(10, 80, 46, 13))
        self.label_8.setObjectName("label_8")
        self.txtZcom = QtWidgets.QLineEdit(self.gbX_2)
        self.txtZcom.setGeometry(QtCore.QRect(40, 80, 111, 20))
        self.txtZcom.setObjectName("txtZcom")
        self.pbGoTo = QtWidgets.QPushButton(self.gbCursor)
        self.pbGoTo.setEnabled(False)
        self.pbGoTo.setGeometry(QtCore.QRect(230, 60, 81, 31))
        self.pbGoTo.setObjectName("pbGoTo")
        self.gbActual = QtWidgets.QGroupBox(self.gbCursor)
        self.gbActual.setGeometry(QtCore.QRect(340, 20, 161, 111))
        self.gbActual.setObjectName("gbActual")
        self.label_11 = QtWidgets.QLabel(self.gbActual)
        self.label_11.setGeometry(QtCore.QRect(10, 20, 46, 13))
        self.label_11.setObjectName("label_11")
        self.txtX = QtWidgets.QLineEdit(self.gbActual)
        self.txtX.setEnabled(False)
        self.txtX.setGeometry(QtCore.QRect(40, 20, 111, 20))
        self.txtX.setObjectName("txtX")
        self.txtY = QtWidgets.QLineEdit(self.gbActual)
        self.txtY.setEnabled(False)
        self.txtY.setGeometry(QtCore.QRect(40, 50, 111, 20))
        self.txtY.setObjectName("txtY")
        self.label_12 = QtWidgets.QLabel(self.gbActual)
        self.label_12.setGeometry(QtCore.QRect(10, 50, 46, 13))
        self.label_12.setObjectName("label_12")
        self.label_14 = QtWidgets.QLabel(self.gbActual)
        self.label_14.setGeometry(QtCore.QRect(10, 80, 46, 13))
        self.label_14.setObjectName("label_14")
        self.txtZ = QtWidgets.QLineEdit(self.gbActual)
        self.txtZ.setEnabled(False)
        self.txtZ.setGeometry(QtCore.QRect(40, 80, 111, 20))
        self.txtZ.setObjectName("txtZ")
        self.pbGetPos = QtWidgets.QPushButton(self.gbCursor)
        self.pbGetPos.setEnabled(False)
        self.pbGetPos.setGeometry(QtCore.QRect(230, 100, 81, 28))
        self.pbGetPos.setObjectName("pbGetPos")
        self.pbGoToMid = QtWidgets.QPushButton(self.gbCursor)
        self.pbGoToMid.setEnabled(False)
        self.pbGoToMid.setGeometry(QtCore.QRect(230, 20, 81, 31))
        self.pbGoToMid.setObjectName("pbGoToMid")
        self.groupBox = QtWidgets.QGroupBox(self.wEssence)
        self.groupBox.setGeometry(QtCore.QRect(580, 160, 531, 101))
        self.groupBox.setObjectName("groupBox")
        self.gbY_2 = QtWidgets.QGroupBox(self.groupBox)
        self.gbY_2.setGeometry(QtCore.QRect(50, 10, 161, 81))
        self.gbY_2.setObjectName("gbY_2")
        self.pbYup = QtWidgets.QPushButton(self.gbY_2)
        self.pbYup.setEnabled(False)
        self.pbYup.setGeometry(QtCore.QRect(60, 10, 41, 23))
        self.pbYup.setObjectName("pbYup")
        self.pbYdown = QtWidgets.QPushButton(self.gbY_2)
        self.pbYdown.setEnabled(False)
        self.pbYdown.setGeometry(QtCore.QRect(60, 50, 41, 23))
        self.pbYdown.setObjectName("pbYdown")
        self.pbXright = QtWidgets.QPushButton(self.gbY_2)
        self.pbXright.setEnabled(False)
        self.pbXright.setGeometry(QtCore.QRect(110, 30, 41, 23))
        self.pbXright.setObjectName("pbXright")
        self.pbXleft = QtWidgets.QPushButton(self.gbY_2)
        self.pbXleft.setEnabled(False)
        self.pbXleft.setGeometry(QtCore.QRect(10, 30, 41, 23))
        self.pbXleft.setObjectName("pbXleft")
        self.gbZ = QtWidgets.QGroupBox(self.groupBox)
        self.gbZ.setGeometry(QtCore.QRect(340, 10, 161, 81))
        self.gbZ.setObjectName("gbZ")
        self.txtStepZ = QtWidgets.QLineEdit(self.gbZ)
        self.txtStepZ.setGeometry(QtCore.QRect(50, 20, 91, 20))
        self.txtStepZ.setObjectName("txtStepZ")
        self.label_9 = QtWidgets.QLabel(self.gbZ)
        self.label_9.setGeometry(QtCore.QRect(10, 20, 46, 13))
        self.label_9.setObjectName("label_9")
        self.pbZup = QtWidgets.QPushButton(self.gbZ)
        self.pbZup.setEnabled(False)
        self.pbZup.setGeometry(QtCore.QRect(50, 50, 41, 23))
        self.pbZup.setObjectName("pbZup")
        self.pbZdown = QtWidgets.QPushButton(self.gbZ)
        self.pbZdown.setEnabled(False)
        self.pbZdown.setGeometry(QtCore.QRect(100, 50, 41, 23))
        self.pbZdown.setObjectName("pbZdown")
        self.pbKeepNV = QtWidgets.QPushButton(self.groupBox)
        self.pbKeepNV.setEnabled(False)
        self.pbKeepNV.setGeometry(QtCore.QRect(230, 30, 81, 31))
        self.pbKeepNV.setObjectName("pbKeepNV")
        self.gbLaser = QtWidgets.QGroupBox(self.wEssence)
        self.gbLaser.setGeometry(QtCore.QRect(350, 20, 211, 61))
        self.gbLaser.setObjectName("gbLaser")
        self.pbLaserOn = QtWidgets.QPushButton(self.gbLaser)
        self.pbLaserOn.setEnabled(False)
        self.pbLaserOn.setGeometry(QtCore.QRect(30, 20, 75, 23))
        self.pbLaserOn.setObjectName("pbLaserOn")
        self.pbLaserOff = QtWidgets.QPushButton(self.gbLaser)
        self.pbLaserOff.setEnabled(False)
        self.pbLaserOff.setGeometry(QtCore.QRect(120, 20, 75, 23))
        self.pbLaserOff.setObjectName("pbLaserOff")
        self.gbHardware = QtWidgets.QGroupBox(self.wEssence)
        self.gbHardware.setGeometry(QtCore.QRect(30, 20, 201, 61))
        self.gbHardware.setObjectName("gbHardware")
        self.pbInitHW = QtWidgets.QPushButton(self.gbHardware)
        self.pbInitHW.setGeometry(QtCore.QRect(10, 20, 75, 23))
        self.pbInitHW.setObjectName("pbInitHW")
        self.pbCleanupHW = QtWidgets.QPushButton(self.gbHardware)
        self.pbCleanupHW.setEnabled(False)
        self.pbCleanupHW.setGeometry(QtCore.QRect(100, 20, 75, 23))
        self.pbCleanupHW.setObjectName("pbCleanupHW")
        self.wMpl = QtWidgets.QWidget(self.wEssence)
        self.wMpl.setGeometry(QtCore.QRect(49, 269, 471, 341))
        self.wMpl.setObjectName("wMpl")
        self.pbSaveData = QtWidgets.QPushButton(self.wEssence)
        self.pbSaveData.setGeometry(QtCore.QRect(430, 610, 93, 28))
        self.pbSaveData.setObjectName("pbSaveData")
        mwConfocal.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(mwConfocal)
        self.statusbar.setObjectName("statusbar")
        mwConfocal.setStatusBar(self.statusbar)
        self.menuBar = QtWidgets.QMenuBar(mwConfocal)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1129, 26))
        self.menuBar.setObjectName("menuBar")
        self.menuFile = QtWidgets.QMenu(self.menuBar)
        self.menuFile.setObjectName("menuFile")
        mwConfocal.setMenuBar(self.menuBar)
        self.actionOpen = QtWidgets.QAction(mwConfocal)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave_As = QtWidgets.QAction(mwConfocal)
        self.actionSave_As.setObjectName("actionSave_As")
        self.actionSave_Defaults = QtWidgets.QAction(mwConfocal)
        self.actionSave_Defaults.setObjectName("actionSave_Defaults")
        self.actionOpen_Defaults = QtWidgets.QAction(mwConfocal)
        self.actionOpen_Defaults.setObjectName("actionOpen_Defaults")
        self.menuFile.addAction(self.actionOpen_Defaults)
        self.menuFile.addAction(self.actionSave_Defaults)
        self.menuBar.addAction(self.menuFile.menuAction())

        self.retranslateUi(mwConfocal)
        QtCore.QMetaObject.connectSlotsByName(mwConfocal)
        mwConfocal.setTabOrder(self.txtStartX, self.txtEndX)
        mwConfocal.setTabOrder(self.txtEndX, self.txtStepX)
        mwConfocal.setTabOrder(self.txtStepX, self.txtStartY)
        mwConfocal.setTabOrder(self.txtStartY, self.txtEndY)
        mwConfocal.setTabOrder(self.txtEndY, self.txtStepY)
        mwConfocal.setTabOrder(self.txtStepY, self.txtZcom)
        mwConfocal.setTabOrder(self.txtZcom, self.txtStepZ)
        mwConfocal.setTabOrder(self.txtStepZ, self.pbZup)
        mwConfocal.setTabOrder(self.pbZup, self.pbZdown)
        mwConfocal.setTabOrder(self.pbZdown, self.pbStart)
        mwConfocal.setTabOrder(self.pbStart, self.pbStop)
        mwConfocal.setTabOrder(self.pbStop, self.txtXcom)
        mwConfocal.setTabOrder(self.txtXcom, self.pbXleft)
        mwConfocal.setTabOrder(self.pbXleft, self.pbXright)
        mwConfocal.setTabOrder(self.pbXright, self.txtYcom)
        mwConfocal.setTabOrder(self.txtYcom, self.pbYup)
        mwConfocal.setTabOrder(self.pbYup, self.pbYdown)
        mwConfocal.setTabOrder(self.pbYdown, self.txtX)
        mwConfocal.setTabOrder(self.txtX, self.txtY)
        mwConfocal.setTabOrder(self.txtY, self.txtZ)
        mwConfocal.setTabOrder(self.txtZ, self.pbGoTo)
        mwConfocal.setTabOrder(self.pbGoTo, self.pbCount)
        mwConfocal.setTabOrder(self.pbCount, self.pbMax)

    def retranslateUi(self, mwConfocal):

        _translate = QtCore.QCoreApplication.translate
        mwConfocal.setWindowTitle(_translate("mwConfocal", "Confocal Imaging"))
        self.gbScan.setTitle(_translate("mwConfocal", "Scan Parameters"))
        self.gbX.setTitle(_translate("mwConfocal", "X"))
        self.label.setText(_translate("mwConfocal", "Start"))
        self.label_4.setText(_translate("mwConfocal", "Step"))
        self.label_3.setText(_translate("mwConfocal", "End"))
        self.gbY.setTitle(_translate("mwConfocal", "Y"))
        self.label_5.setText(_translate("mwConfocal", "Start"))
        self.label_6.setText(_translate("mwConfocal", "Step"))
        self.label_7.setText(_translate("mwConfocal", "End"))
        self.pbStart.setText(_translate("mwConfocal", "Start"))
        self.pbStop.setText(_translate("mwConfocal", "Stop"))
        self.gbSpeed.setTitle(_translate("mwConfocal", "Speed"))
        self.label_16.setText(_translate("mwConfocal", "Step Frequency (Hz)"))
        self.cbFreq.setItemText(0, _translate("mwConfocal", "3750"))
        self.cbFreq.setItemText(1, _translate("mwConfocal", "2000"))
        self.cbFreq.setItemText(2, _translate("mwConfocal", "1000"))
        self.cbFreq.setItemText(3, _translate("mwConfocal", "500"))
        self.cbFreq.setItemText(4, _translate("mwConfocal", "100"))
        self.cbFreq.setItemText(5, _translate("mwConfocal", "60"))
        self.cbFreq.setItemText(6, _translate("mwConfocal", "50"))
        self.pbCenter.setText(_translate("mwConfocal", "Center Cursor"))
        self.pbFullScale.setText(_translate("mwConfocal", "Full Scale"))
        self.label_2.setText(_translate("mwConfocal", "Range"))
        self.txtRange.setText(_translate("mwConfocal", "10"))
        self.gbCounts.setTitle(_translate("mwConfocal", "Counts"))
        self.pbCount.setText(_translate("mwConfocal", "On"))
        self.pbMax.setText(_translate("mwConfocal", "Max"))
        self.cbCountFreq.setItemText(0, _translate("mwConfocal", "1"))
        self.cbCountFreq.setItemText(1, _translate("mwConfocal", "3"))
        self.cbCountFreq.setItemText(2, _translate("mwConfocal", "5"))
        self.cbCountFreq.setItemText(3, _translate("mwConfocal", "10"))
        self.label_15.setText(_translate("mwConfocal", "Hz"))
        self.pbSlide.setText(_translate("mwConfocal", "Set"))
        self.gbCursor.setTitle(_translate("mwConfocal", "Cursor"))
        self.gbX_2.setTitle(_translate("mwConfocal", "Cursor"))
        self.label_10.setText(_translate("mwConfocal", "X"))
        self.label_13.setText(_translate("mwConfocal", "Y"))
        self.label_8.setText(_translate("mwConfocal", "Z"))
        self.pbGoTo.setText(_translate("mwConfocal", "Go!"))
        self.gbActual.setTitle(_translate("mwConfocal", "Actual"))
        self.label_11.setText(_translate("mwConfocal", "X"))
        self.label_12.setText(_translate("mwConfocal", "Y"))
        self.label_14.setText(_translate("mwConfocal", "Z"))
        self.pbGetPos.setText(_translate("mwConfocal", "<--"))
        self.pbGoToMid.setText(_translate("mwConfocal", "Go to Mid"))
        self.groupBox.setTitle(_translate("mwConfocal", "Move"))
        self.gbY_2.setTitle(_translate("mwConfocal", "X-Y"))
        self.pbYup.setText(_translate("mwConfocal", "??"))
        self.pbYdown.setText(_translate("mwConfocal", "??"))
        self.pbXright.setText(_translate("mwConfocal", ">"))
        self.pbXleft.setText(_translate("mwConfocal", "<"))
        self.gbZ.setTitle(_translate("mwConfocal", "Z"))
        self.label_9.setText(_translate("mwConfocal", "Step"))
        self.pbZup.setText(_translate("mwConfocal", "??"))
        self.pbZdown.setText(_translate("mwConfocal", "??"))
        self.pbKeepNV.setText(_translate("mwConfocal", "KeepNV"))
        self.gbLaser.setTitle(_translate("mwConfocal", "Laser"))
        self.pbLaserOn.setText(_translate("mwConfocal", "On"))
        self.pbLaserOff.setText(_translate("mwConfocal", "Off"))
        self.gbHardware.setTitle(_translate("mwConfocal", "Hardware"))
        self.pbInitHW.setText(_translate("mwConfocal", "Initialize"))
        self.pbCleanupHW.setText(_translate("mwConfocal", "Reset"))
        self.pbSaveData.setText(_translate("mwConfocal", "Save Data"))
        self.menuFile.setTitle(_translate("mwConfocal", "File"))
        self.actionOpen.setText(_translate("mwConfocal", "Open"))
        self.actionSave_As.setText(_translate("mwConfocal", "Save As"))
        self.actionSave_Defaults.setText(_translate("mwConfocal", "Save Defaults"))
        self.actionOpen_Defaults.setText(_translate("mwConfocal", "Open Defaults"))

from guiqwt.plot import CurveWidget
