'''
Created on Apr 17, 2015

@author: Kai Zhang
'''

# Modified Nov. 4, 2019 by Gurudev
# primary changes are for Python3 and Qt5 upgrade

from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow, QApplication
import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar, FigureCanvasQTAgg as FigureCanvas
from matplotlib import cm
from matplotlib.figure import Figure
from guiqwt.builder import make
import sys,numpy
from apscheduler.schedulers.background import BackgroundScheduler

#from Confocal.SQL import Database
import os

#from GUI.GUI import Ui_mwConfocal
from GUI.Crosshair import Crosshair
from Hardware.ADWIN_MCL import ADWIN_MCL
from Hardware.Threads import CountThread,PositionThread,ScanThread,MaxThread,KeepThread
import SQL_confocal



import datetime

from pathlib import Path
# thisdir = Path('.')
# qtdesignerfile = thisdir /'GUI/GUIv1.ui'

Ui_mwConfocal,QtBaseClass = uic.loadUiType('GUIv2.ui')

def counted(f):
    """decorator to keep track of how many times a function is called. used by the update_image function to only
    update image after certain number of lines of data have been taken"""
    def wrapped(*args, **kwargs):
        wrapped.calls += 1
        return f(*args, **kwargs)

    wrapped.calls = 0
    return wrapped

class GUI_Wrapper(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        QtWidgets.QWidget.__init__(self,parent)
        self.ui=Ui_mwConfocal()
        self.ui.setupUi(self)
        
        # Image matplotlib widget
        fig=Figure()
        self.ui.mplMap=FigureCanvas(fig)
        self.ui.mplMap.setParent(self.ui.wMpl)
        self.ui.mplMap.axes=fig.add_subplot(111)
        self.ui.mplMap.setGeometry(QtCore.QRect(QtCore.QPoint(0,0),self.ui.wMpl.size()))
        # Toolbar widget for image
        self.ui.mplToolbar = NavigationToolbar(self.ui.mplMap,self.ui.wToolbar)
        self.ui.mplToolbar.setGeometry(QtCore.QRect(0,0, self.ui.wToolbar.size().width(), 31))
        self.ui.mplToolbar.setSizePolicy(QtWidgets.QSizePolicy.Fixed,QtWidgets.QSizePolicy.Fixed)
        self.ui.mplToolbar.setSizePolicy(QtWidgets.QSizePolicy.Fixed,QtWidgets.QSizePolicy.Fixed)
        self.ui.mplToolbar.setParent(self.ui.wToolbar)

        #Defining initial conditions for other parameters
        self.DiaSampID = None
        self.DiaSampDesc = ''
        self.NVID = None
        self.ObjModNum = None
        self.BF = ''
        self.BWSize = None
        self.LWave = 532
        self.LPow = None
        self.ConvX = 1
        self.ConvY = 1
        self. ConvZ = 1

        # Hardware
        self.hardware = ADWIN_MCL()

        
        # Sets up connections
        self.setup_conn()
        self.load_defaults()

        # Each of the 4 possible thread types is defined here
        self.sThread = ScanThread(self.hardware)
        self.sThread.init_image.connect(self.init_image)

        self.sThread.update_image.connect(self.update_image) # when the signal is received, update the front panel image
        self.sThread.finished.connect(self.finish)
        
        self.cThread = CountThread(self.hardware)
        self.cThread.counts.connect(self.updateCounts)
        self.cThread.finished.connect(self.countStopped)
        
        self.pThread = PositionThread(self.hardware)
        self.pThread.done.connect(self.gone_to)
        
        self.mThread = MaxThread(self.hardware)
        self.mThread.counts.connect(self.updateMaxCounts)
        self.mThread.finished.connect(self.done_max)
        
        self.kThread = KeepThread(self)
        self.kThread.done.connect(self.doneKeeping)
        # Initialize counts display
        self.count_array=[0]*100
        self.curve_item = make.curve([], [], color='b')
        self.ui.curvewidget.plot.add_item(self.curve_item)
        self.ui.curvewidget.plot.set_antialiasing(True)
        self.ui.curvewidget.plot.set_titles("Counts vs Time", "Seconds", "Counts")
        
        # Initialize cursor object
        self.cur=None

        #Tracking NV
        self.NV_Tracking = False
        self.tracking_scheduler = BackgroundScheduler()
        
        
            
        
    def setup_conn(self):
        # PushButtons and LineEdits
        self.ui.pbStart.clicked.connect(self.start)
        self.ui.pbStop.clicked.connect(self.stop)
        self.ui.pbCount.clicked.connect(self.count)
        self.ui.cbCountFreq.activated.connect(self.countRate)
        self.ui.pbMax.clicked.connect(self.maximize_counts)
        self.ui.pbKeepNV.clicked.connect(self.keepNV)
        self.ui.pbCenter.clicked.connect(self.center)
        self.ui.pbFullScale.clicked.connect(self.fullscale)
        
        self.ui.pbGetPos.clicked.connect(self.getPosition)
        self.ui.pbGoTo.clicked.connect(self.goto)
        self.ui.pbGoToMid.clicked.connect(self.gotoMid)
        self.ui.pbXleft.clicked.connect(lambda:self.goto('x-'))
        self.ui.pbXright.clicked.connect(lambda:self.goto('x+'))
        self.ui.pbYdown.clicked.connect(lambda:self.goto('y-'))
        self.ui.pbYup.clicked.connect(lambda:self.goto('y+'))
        self.ui.pbZdown.clicked.connect(lambda:self.goto('z-'))
        self.ui.pbZup.clicked.connect(lambda:self.goto('z+'))

        self.ui.pbLaserOn.clicked.connect(self.hardware.laser_on)
        self.ui.pbLaserOff.clicked.connect(self.hardware.laser_off)

        self.ui.pbCleanupHW.clicked.connect(self.hwReset)
        self.ui.pbInitHW.clicked.connect(self.hwInit)

        # Default Scan Freq
        self.ui.cbFreq.setCurrentIndex(3)


        # File menu

        self.ui.actionOpen_Defaults.triggered.connect(self.load_defaults)
        self.ui.actionSave_Defaults.triggered.connect(self.save_defaults)

        #Connecting Push Buttons for NV Tracking

        self.ui.pbNVTrackingOn.clicked.connect(self.trackingOn)
        self.ui.pbNVTrackingOff.clicked.connect(self.trackingOff)
        self.ui.pbNVTrackingOff.setEnabled(False)


        #connecting other parameters buttons here
        self.ui.diaSampleIDLineEdit.editingFinished.connect(self.updateSampID)
        self.ui.diaSampleDescLineEdit.editingFinished.connect(self.updateSampDesc)
        self.ui.nvIDLineEdit.editingFinished.connect(self.updateNVID)
        self.ui.objModNumLineEdit.editingFinished.connect(self.updateModNum)
        self.ui.bandFiltersLineEdit.editingFinished.connect(self.updateBF)
        self.ui.beamWaistLineEdit.editingFinished.connect(self.updateBWS)
        self.ui.lasWaveLineEdit.editingFinished.connect(self.updateLW)
        self.ui.lasPowerLineEdit.editingFinished.connect(self.updateLP)
        self.ui.convXLineEdit.editingFinished.connect(self.updateCX)
        self.ui.convYLineEdit.editingFinished.connect(self.updateCY)
        self.ui.convZLineEdit.editingFinished.connect(self.updateCZ)
        
    #functions for other parameters
    def updateSampID(self):
        self.DiaSampID = int(self.ui.diaSampleIDLineEdit.text())

    def updateSampDesc(self):
        self.DiaSampDesc = str(self.ui.diaSampleDescLineEdit.text())

    def updateNVID(self):
        self.NVID = int(self.ui.nvIDLineEdit.text())

    def updateModNum(self):
        self.ObjModNum = int(self.ui.objModNumLineEdit.text())

    def updateBF(self):
        self.BF = str(self.ui.bandFiltersLineEdit.text())

    def updateBWS(self):
        self.BWSize = int(self.ui.beamWaistLineEdit.text())

    def updateLW(self):
        self.LWave = int(self.ui.lasWaveLineEdit.text())

    def updateLP(self):
        self.LPow = int(self.ui.lasPowerLineEdit.text())

    def updateCX(self):
        self.ConvX = int(self.ui.convXLineEdit.text())

    def updateCY(self):
        self.ConvY = int(self.ui.convYLineEdit.text())

    def updateCZ(self):
        self.ConvZ = int(self.ui.convZLineEdit.text())
        
    #loading in defualt values
    def load_defaults(self,fName = 'defaults.txt'):
        f=open(fName,'r')
        d={}
        for line in f.readlines():
            if line[-1]=='\n':
                line=line[:-1]
            [key,value]=line.split('=')
            d[key]=value
        f.close()
        dic={'STARTX':self.ui.txtStartX,
             'STARTY':self.ui.txtStartY,
             'ENDX':self.ui.txtEndX,
             'ENDY':self.ui.txtEndY,
             'STEPX':self.ui.txtStepX,
             'STEPY':self.ui.txtStepY,
             'ZVAL':self.ui.txtZcom,
             'STEPZ':self.ui.txtStepZ,
             'CURSORX':self.ui.txtXcom,
             'CURSORY':self.ui.txtYcom
             }
        for key,value in d.items():
            dic.get(key).setText(value)
        
    def save_defaults(self,fName = 'defaults.txt'):
        pairList = []
        pairList.append(("STARTX",self.ui.txtStartX.text()))
        pairList.append(("STARTY",self.ui.txtStartY.text()))
        pairList.append(("ENDX",self.ui.txtEndX.text()))
        pairList.append(("ENDY",self.ui.txtEndY.text()))
        pairList.append(("STEPX",self.ui.txtStepX.text()))
        pairList.append(("STEPY",self.ui.txtStepY.text()))
        pairList.append(("ZVAL",self.ui.txtZcom.text()))
        pairList.append(("STEPZ",self.ui.txtStepZ.text()))
        pairList.append(("CURSORX",self.ui.txtXcom.text()))
        pairList.append(("CURSORY",self.ui.txtYcom.text()))
        ofile=open(fName,'w')
        for pair in pairList:
            ofile.write(pair[0] + "=" + pair[1] + "\n")
        ofile.close()

    def hwInit(self):
        if self.hardware.initialize()==0:
            self.ui.pbNVTrackingOn.setEnabled(True)
            self.ui.pbCount.setEnabled(True)
            self.ui.pbGoTo.setEnabled(True)
            self.ui.pbGoToMid.setEnabled(True)
            self.ui.pbLaserOn.setEnabled(True)
            self.ui.pbLaserOff.setEnabled(True)
            self.ui.pbMax.setEnabled(True)
            self.ui.pbKeepNV.setEnabled(True)
            self.ui.pbStart.setEnabled(True)
            self.ui.pbXleft.setEnabled(True)
            self.ui.pbXright.setEnabled(True)
            self.ui.pbYdown.setEnabled(True)
            self.ui.pbYup.setEnabled(True)
            self.ui.pbZdown.setEnabled(True)
            self.ui.pbZup.setEnabled(True)
            self.initPosition()
            self.ui.statusbar.showMessage('Hardware Initialized Successfully.')
        else:
            self.ui.statusbar.showMessage('Hardware did not initialize.')
        self.ui.pbInitHW.setEnabled(False)
        self.ui.pbCleanupHW.setEnabled(True)

    def hwReset(self):
        self.ui.pbNVTrackingOn.setEnabled(False)
        self.ui.pbCount.setEnabled(False)
        self.ui.pbGoTo.setEnabled(False)
        self.ui.pbGoToMid.setEnabled(False)
        self.ui.pbLaserOn.setEnabled(False)
        self.ui.pbLaserOff.setEnabled(False)
        self.ui.pbMax.setEnabled(False)
        self.ui.pbKeepNV.setEnabled(False)
        self.ui.pbStart.setEnabled(False)
        self.ui.pbStop.setEnabled(False)
        self.ui.pbXleft.setEnabled(False)
        self.ui.pbXright.setEnabled(False)
        self.ui.pbYdown.setEnabled(False)
        self.ui.pbYup.setEnabled(False)
        self.ui.pbZdown.setEnabled(False)
        self.ui.pbZup.setEnabled(False)
        if self.hardware.cleanup()==0:
            self.ui.statusbar.showMessage('Hardware Reset Successfully.')
        else:
            self.ui.statusbar.showMessage('Hardware Reset Failed.')
        self.ui.pbInitHW.setEnabled(True)
        self.ui.pbCleanupHW.setEnabled(False)

    def count(self):
        self.ui.statusbar.showMessage('Counting...')
        self.ui.pbMax.setEnabled(False)
        self.ui.pbNVTrackingOn.setEnabled(False)
        if not self.kThread.running:
            self.ui.pbKeepNV.setEnabled(False)
        self.ui.pbStart.setEnabled(False)
        self.ui.pbCount.setText('Off')
        
        self.cThread.start()
        self.ui.pbCount.clicked.disconnect()
        self.ui.pbCount.clicked.connect(self.countStop)
        self.ui.cbCountFreq.setEnabled(True)
        
    def countStop(self):
        self.cThread.stop_counting()
        
    def countStopped(self):
        self.ui.statusbar.clearMessage()
        self.ui.pbMax.setEnabled(True)
        self.ui.pbNVTrackingOn.setEnabled(True)
        self.ui.pbKeepNV.setEnabled(True)
        self.ui.pbStart.setEnabled(True)
        self.ui.pbCount.setText('On')
        self.ui.cbCountFreq.setEnabled(False)
        self.ui.cbCountFreq.setCurrentIndex(0)
        self.ui.pbCount.clicked.disconnect()
        self.ui.pbCount.clicked.connect(self.count)
        
    def countRate(self):
        rate = int(self.ui.cbCountFreq.currentText())
        self.cThread.change_rate(rate)
    
    def updateCounts(self,data):
        self.ui.lcdNumber.display(int(data))
        self.count_array=self.count_array[1:]+[data]
        y_array=self.count_array
        x_array=numpy.arange(10,step=0.1)
        self.curve_item.set_data(x_array, y_array)
        self.curve_item.plot().replot()

    def initPosition(self):
        nd=self.hardware.nd
        handle=self.hardware.nd_handle
        x = nd.SingleReadN('x', handle)
        y = nd.SingleReadN('y', handle)
        z = nd.SingleReadN('z', handle)
        x = round(x,3)
        y = round(y,3)
        z = round(z,3)
        self.ui.txtX.setText(str(x))
        self.ui.txtY.setText(str(y))
        self.ui.txtZ.setText(str(z))
        self.ui.pbGetPos.setEnabled(True)

    def getPosition(self):    
        self.ui.txtXcom.setText(self.ui.txtX.text())
        self.ui.txtYcom.setText(self.ui.txtY.text())
        self.ui.txtZcom.setText(self.ui.txtZ.text())
        
    def goto(self,*args):
        dic={'x+':lambda:self.ui.txtXcom.setText( str(float(self.ui.txtXcom.text())+float(self.ui.txtStepX.text())) ),
             'x-':lambda:self.ui.txtXcom.setText( str(float(self.ui.txtXcom.text())-float(self.ui.txtStepX.text())) ),
             'y+':lambda:self.ui.txtYcom.setText( str(float(self.ui.txtYcom.text())+float(self.ui.txtStepY.text())) ),
             'y-':lambda:self.ui.txtYcom.setText( str(float(self.ui.txtYcom.text())-float(self.ui.txtStepY.text())) ),
             'z+':lambda:self.ui.txtZcom.setText( str(float(self.ui.txtZcom.text())+float(self.ui.txtStepZ.text())) ),
             'z-':lambda:self.ui.txtZcom.setText( str(float(self.ui.txtZcom.text())-float(self.ui.txtStepZ.text())) )}
        dic.get(args[0],lambda:0)()
        x=float(self.ui.txtXcom.text())
        y=float(self.ui.txtYcom.text())
        z=float(self.ui.txtZcom.text())
        self.pThread.command=[x,y,z]
        
        self.ui.pbStart.setEnabled(False)
        self.pThread.start()
        
    def gotoMid(self):
        self.ui.txtXcom.setText('50')
        self.ui.txtYcom.setText('50')
        self.ui.txtZcom.setText('50')
        self.goto(0)
        
    def gone_to(self,x,y,z):
        self.ui.txtX.setText(str(x))
        self.ui.txtY.setText(str(y))
        self.ui.txtZ.setText(str(z))
        if not self.cThread.counting:
            self.ui.pbStart.setEnabled(True)

    def fullscale(self):
        '''

        edited 7/25/2019: 0 and 100 sometimes return argument error/out of range. all scans by default will be from 1 to 99 until issue resolved to
        prevent damage to the stage.

        '''


        self.ui.txtStartX.setText(str(5.0))
        self.ui.txtStartY.setText(str(5.0))
        self.ui.txtEndX.setText(str(95.0))
        self.ui.txtEndY.setText(str(95.0))
        self.ui.txtStepX.setText(str(1.0))
        self.ui.txtStepY.setText(str(1.0))

    def center(self):
        xval = round(float(self.ui.txtXcom.text()),1)
        yval = round(float(self.ui.txtYcom.text()),1)
        d= float(self.ui.txtRange.text())
        self.ui.txtStartX.setText(str(xval - d/2))
        self.ui.txtStartY.setText(str(yval-d/2))
        self.ui.txtEndX.setText(str(xval + d/2))
        self.ui.txtEndY.setText(str(yval + d/2))
        self.ui.txtStepX.setText(str(d/100))
        self.ui.txtStepY.setText(str(d/100))

    def start(self):
        self.ui.statusbar.showMessage('Scanning...')
        self.ui.pbNVTrackingOn.setEnabled(False)
        self.ui.pbCount.setEnabled(False)
        self.ui.pbGoTo.setEnabled(False)
        self.ui.pbGoToMid.setEnabled(False)
        self.ui.pbMax.setEnabled(False)
        self.ui.pbKeepNV.setEnabled(False)
        self.ui.pbXleft.setEnabled(False)
        self.ui.pbXright.setEnabled(False)
        self.ui.pbYdown.setEnabled(False)
        self.ui.pbYup.setEnabled(False)
        self.ui.pbZdown.setEnabled(False)
        self.ui.pbZup.setEnabled(False)
        self.ui.pbStart.setEnabled(False)
        self.ui.pbStop.setEnabled(True)
        #new variables
        self.ui.diaSampleIDLineEdit.setEnabled(False)
        self.ui.diaSampleDescLineEdit.setEnabled(False)
        self.ui.nvIDLineEdit.setEnabled(False)
        self.ui.objModNumLineEdit.setEnabled(False)
        self.ui.bandFiltersLineEdit.setEnabled(False)
        self.ui.beamWaistLineEdit.setEnabled(False)
        self.ui.lasWaveLineEdit.setEnabled(False)
        self.ui.lasPowerLineEdit.setEnabled(False)
        self.ui.convXLineEdit.setEnabled(False)
        self.ui.convYLineEdit.setEnabled(False)
        self.ui.convZLineEdit.setEnabled(False)

        #do not need to pass new varables into sThread
        self.sThread.parameters=(float(self.ui.txtStartX.text()),
                                 float(self.ui.txtEndX.text()),
                                 float(self.ui.txtStepX.text()),
                                 float(self.ui.txtStartY.text()),
                                 float(self.ui.txtEndY.text()),
                                 float(self.ui.txtStepY.text()),
                                 float(self.ui.txtZcom.text()),
                                 float(self.ui.cbFreq.currentText())
                                 )
        self.sThread.start()
        
    def init_image(self, C):
        self.C = C
        self.C[0][0] = 1

        mesh = self.ui.mplMap.axes.imshow(self.C, cmap=cm.get_cmap('gist_earth'), vmin=0, vmax=self.C.max(),
                                          extent=[float(self.ui.txtStartX.text()), float(self.ui.txtEndX.text()),
                                                  float(self.ui.txtStartY.text()), float(self.ui.txtEndY.text())],
                                          interpolation='nearest', origin='lower')

        self.ui.mplMap.axes.set_ylim([float(self.ui.txtStartY.text()), float(self.ui.txtEndY.text())])
        self.ui.mplMap.axes.set_xlim([float(self.ui.txtStartX.text()), float(self.ui.txtEndX.text())])

        try:
            self.cbar
        except:  # if self.cbar is not defined 
            self.cbar = self.ui.mplMap.figure.colorbar(mesh)

        self.ui.mplMap.figure.tight_layout()
        
        if self.cur is None:
            self.cur = Crosshair(self.ui.mplMap.axes, useblit=True, color='yellow', linewidth=0.5)
            self.cur.update_loc.connect(self.update_com)

            #self.connect(self.cur,QtCore.SIGNAL("update_loc(float,float)"),self.update_com)
            
        self.ui.mplMap.figure.canvas.draw()
        
        self.ui.txtXcom.textChanged.connect(self.update_cursor)
        self.ui.txtYcom.textChanged.connect(self.update_cursor)
        
        self.ui.pbSlide.setEnabled(True)
        self.ui.pbSlide.clicked.connect(self.slide)
        self.ui.pbSaveData.clicked.connect(self.save_data)

    @counted
    def update_image(self, C):
        num_lines_to_take_before_plotting = 2  # adjust the value here to update the image slower or faster
        if self.update_image.calls % num_lines_to_take_before_plotting == 0:
            self.C = C
            mesh = self.ui.mplMap.axes.imshow(self.C, cmap=cm.get_cmap('gist_earth'), vmin=0, vmax=self.C.max(),
                                              extent=[float(self.ui.txtStartX.text()), float(self.ui.txtEndX.text()),
                                                      float(self.ui.txtStartY.text()), float(self.ui.txtEndY.text())],
                                              interpolation='nearest', origin='lower')

            self.cbar.mappable.set_clim(0, self.C.max())
            self.cbar.draw_all()

            self.ui.mplMap.figure.canvas.draw()
        else:
            pass

    def finish(self):
        self.update_image(self.C)
        self.stop()
    
    def stop(self):
        self.sThread.scanning=False
        self.ui.statusbar.showMessage('Scanning stopped.')
        self.ui.pbNVTrackingOn.setEnabled(True)
        self.ui.pbCount.setEnabled(True)
        self.ui.pbGoTo.setEnabled(True)
        self.ui.pbGoToMid.setEnabled(True)
        self.ui.pbMax.setEnabled(True)
        self.ui.pbKeepNV.setEnabled(True)
        self.ui.pbXleft.setEnabled(True)
        self.ui.pbXright.setEnabled(True)
        self.ui.pbYdown.setEnabled(True)
        self.ui.pbYup.setEnabled(True)
        self.ui.pbZdown.setEnabled(True)
        self.ui.pbZup.setEnabled(True)
        self.ui.pbStart.setEnabled(True)
        self.ui.pbStop.setEnabled(False)
        #new variables
        self.ui.diaSampleIDLineEdit.setEnabled(True)
        self.ui.diaSampleDescLineEdit.setEnabled(True)
        self.ui.nvIDLineEdit.setEnabled(True)
        self.ui.objModNumLineEdit.setEnabled(True)
        self.ui.bandFiltersLineEdit.setEnabled(True)
        self.ui.beamWaistLineEdit.setEnabled(True)
        self.ui.lasWaveLineEdit.setEnabled(True)
        self.ui.lasPowerLineEdit.setEnabled(True)
        self.ui.convXLineEdit.setEnabled(True)
        self.ui.convYLineEdit.setEnabled(True)
        self.ui.convZLineEdit.setEnabled(True)

        self.initPosition()
        self.update_cursor()


    def update_cursor(self):
        if self.cur is not None and len(self.ui.txtXcom.text())>0 and len(self.ui.txtYcom.text()) > 0:
            self.cur.setX(float(self.ui.txtXcom.text()))
            self.cur.setY(float(self.ui.txtYcom.text()))

    def update_com(self, x, y):
        self.ui.txtXcom.setText(str(round(x, 3)))
        self.ui.txtYcom.setText(str(round(y, 3)))
        
    def slide(self):
        val = self.ui.vsMax.value()
        
        mesh=self.ui.mplMap.axes.imshow(self.C, cmap=cm.get_cmap('gist_earth'), vmin=0, vmax=self.C.max()*val/100.0,
           extent=[float(self.ui.txtStartX.text()), float(self.ui.txtEndX.text()), float(self.ui.txtStartY.text()), float(self.ui.txtEndY.text())],
           interpolation='nearest', origin='lower')
        
        self.cbar.mappable.set_clim(0, self.C.max()*val/100.0)
        self.cbar.draw_all()
        
        self.ui.mplMap.figure.canvas.draw()

    def save_data(self):
        xcoord = []
        ycoord = []
        counts = []

        for each_datapoint in self.sThread.Actual:
            xcoord.append(each_datapoint[0])
            ycoord.append(each_datapoint[1])
            counts.append(each_datapoint[2])

        sql = SQL_Test.SQL_object()
        sql.insert(self.DiaSampID, self.DiaSampDesc, self.NVID, self.ObjModNum, self.BF, self.BWSize, self.LWave,
                   self.LPow, self.ConvX, self.ConvY, self.ConvZ, xcoord, ycoord, counts)


    def maximize_counts(self):
        self.ui.pbNVTrackingOn.setEnabled(False)
        self.ui.pbCount.setEnabled(False)
        self.ui.pbGoTo.setEnabled(False)
        self.ui.pbGoToMid.setEnabled(False)
        self.ui.pbMax.setEnabled(False)
        if not self.kThread.running:
            self.ui.pbKeepNV.setEnabled(False)
        self.ui.pbXleft.setEnabled(False)
        self.ui.pbXright.setEnabled(False)
        self.ui.pbYdown.setEnabled(False)
        self.ui.pbYup.setEnabled(False)
        self.ui.pbZdown.setEnabled(False)
        self.ui.pbZup.setEnabled(False)
        self.ui.pbStart.setEnabled(False)
        self.mThread.start()

    def done_max(self):

        if self.NV_Tracking:
            self.ui.pbNVTrackingOff.setEnabled(True)
        else:
            self.ui.pbNVTrackingOn.setEnabled(True)
            self.ui.pbCount.setEnabled(True)
            self.ui.pbGoTo.setEnabled(True)
            self.ui.pbGoToMid.setEnabled(True)
            self.ui.pbMax.setEnabled(True)
            self.ui.pbKeepNV.setEnabled(True)
            self.ui.pbXleft.setEnabled(True)
            self.ui.pbXright.setEnabled(True)
            self.ui.pbYdown.setEnabled(True)
            self.ui.pbYup.setEnabled(True)
            self.ui.pbZdown.setEnabled(True)
            self.ui.pbZup.setEnabled(True)
            self.ui.pbStart.setEnabled(True)
            self.initPosition()

    def updateMaxCounts(self,data):
        self.ui.lcdNumber.display(int(data))
        self.count_array=self.count_array[1:]+[data]
        y_array=self.count_array
        x_array=numpy.arange(10,step=0.1)
        self.curve_item.set_data(x_array, y_array)
        self.curve_item.plot().replot()

    def keepNV(self):
        self.ui.pbKeepNV.clicked.disconnect()
        self.ui.pbKeepNV.setEnabled(False)
        self.ui.pbKeepNV.setText('Done')
        self.ui.pbKeepNV.clicked.connect(self.doneKeeping)
        self.kThread.start()

    def stopKeeping(self):
        self.kThread.running=False


    def doneKeeping(self):
        self.ui.pbKeepNV.clicked.disconnect()
        self.ui.pbKeepNV.setText('KeepNV')
        self.ui.pbKeepNV.clicked.connect(self.keepNV)
        self.ui.pbKeepNV.setEnabled(True)


    def closeEvent(self, event):
        if self.sThread.scanning or self.mThread.maximizing:
            QtWidgets.QMessageBox.information(self,"Message","You have a scan running.  Please stop before closing.")

            event.ignore()
            return

        quit_msg = "Do you want to save parameters as defaults?"

        reply = QtWidgets.QMessageBox.question(self, 'Message',
                                            quit_msg, QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Cancel)

        if reply == QtWidgets.QMessageBox.Yes:
            self.save_defaults()
            self.hardware.cleanup()
            exit(0)

        elif reply == QtWidgets.QMessageBox.No:
            self.hardware.cleanup()
            exit(0)

        else:
            event.ignore()


    def trackingOn(self):
        print("NV tracking Started\n")
        self.NV_Tracking = True
        self.ui.pbNVTrackingOn.setEnabled(False)
        self.ui.pbCount.setEnabled(False)
        self.ui.pbGoTo.setEnabled(False)
        self.ui.pbGoToMid.setEnabled(False)
        self.ui.pbXleft.setEnabled(False)
        self.ui.pbXright.setEnabled(False)
        self.ui.pbYdown.setEnabled(False)
        self.ui.pbYup.setEnabled(False)
        self.ui.pbZdown.setEnabled(False)
        self.ui.pbZup.setEnabled(False)
        self.ui.pbStart.setEnabled(False)
        self.ui.pbMax.setEnabled(False)
        self.ui.pbNVTrackingOff.setEnabled(True)

        minutes = 30

        self.tracking_scheduler.add_job(self.trackingMax, 'interval', seconds = minutes*60)
        self.tracking_scheduler.start()

    def trackingMax(self):
        print("Maximization started\n")
        self.ui.pbNVTrackingOff.setEnabled(False)
        self.mThread.start()

    def trackingOff(self):
        self.tracking_scheduler.shutdown()
        self.tracking_scheduler = BackgroundScheduler()
        self.NV_Tracking = False

        self.ui.pbNVTrackingOff.setEnabled(False)
        self.ui.pbNVTrackingOn.setEnabled(True)


        self.ui.pbCount.setEnabled(True)
        self.ui.pbGoTo.setEnabled(True)
        self.ui.pbGoToMid.setEnabled(True)
        self.ui.pbXleft.setEnabled(True)
        self.ui.pbXright.setEnabled(True)
        self.ui.pbYdown.setEnabled(True)
        self.ui.pbYup.setEnabled(True)
        self.ui.pbZdown.setEnabled(True)
        self.ui.pbZup.setEnabled(True)
        self.ui.pbStart.setEnabled(True)
        self.ui.pbMax.setEnabled(True)

        print("NV tracking Stopped\n")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    UIWindow = GUI_Wrapper()
    UIWindow.show()
    app.exec_()


