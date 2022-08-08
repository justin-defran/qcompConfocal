__author__ = 'Bradley'
from matplotlib.widgets import Cursor
from PyQt5 import QtCore # modified Nov. 4, 2019 by Gurudev


class Crosshair(Cursor,QtCore.QObject):
    
    SIGNAL_update_loc=QtCore.pyqtSignal(float,float,name='update_loc')
    
    def __init__(self, ax, hOn=True, vOn=True, ub=False,
                 **lineprops):
        Cursor.__init__(self,ax,**lineprops)
        QtCore.QObject.__init__(self)
        self.connect_event('button_press_event',self.press)
        self.connect_event('button_release_event',self.release)
        self.pressed = False
        self.lineh.set_ydata((0,0))
        self.linev.set_xdata((0,0))

        self.linev.set_visible(True)
        self.lineh.set_visible(True)

        self.firstrun = True
        self.visible=True
        
        lim=ax.get_ylim()
        self.resY=(lim[1]-lim[0])/10.0
        lim=ax.get_xlim()
        self.resX=(lim[1]-lim[0])/10.0
        
        
    def getX(self):
        return self.linev.get_data()[0]
    def setX(self,x):
        self.linev.set_xdata((x,x))
        self.linev.set_visible(True)
        self._update()
    def setY(self,x):
        self.lineh.set_ydata((x,x))
        self.lineh.set_visible(True)
        self._update()
    def press(self,event):
        #print "You clicked me bro"
        if event.inaxes is not None:
            x,y = event.xdata, event.ydata
            xdat,_ = self.linev.get_data()
            _,ydat = self.lineh.get_data()
            c_x,c_y = xdat[0],ydat[0]
            if abs(x-c_x) < self.resX and abs(y-c_y) < self.resY:
                self.pressed = True


    def release(self,event):
        self.pressed = False
        xdat,_ = self.linev.get_data()
        _,ydat = self.lineh.get_data()

        self.update_loc.emit(xdat[0],ydat[0])
        #I'll add the "Snap to" functionality here, if necessary
    def seeMe(self):
        self.visible=True
        self.linev.set_visible(True)
        self.lineh.set_visible(True)
        #self._update()
        self.firstrun = False
        #pylab.draw()


    def onmove(self, event):
        #print "I moved baby", event.xdata,event.ydata
        """on mouse motion draw the cursor if visible"""
        if self.firstrun:
            self.linev.set_visible(True)
            self.lineh.set_visible(True)
            self._update()
            self.firstrun = False
            return

        self.linev.set_visible(True)
        self.lineh.set_visible(True)
        self._update()
        self.firstrun = False

        if not self.pressed:
            return

        if self.ignore(event):
            return
        if not self.canvas.widgetlock.available(self):
            print("No widget lock")
            return
        if event.inaxes != self.ax:
            self.linev.set_visible(False)
            self.lineh.set_visible(False)

            if self.needclear:
                self.canvas.draw()
                self.needclear = False
            return
        self.needclear = True
        if not self.visible:
            return

        self.linev.set_xdata((event.xdata, event.xdata))

        self.lineh.set_ydata((event.ydata, event.ydata))
        self.linev.set_visible(self.visible and self.vertOn)
        self.lineh.set_visible(self.visible and self.horizOn)

        self._update()
