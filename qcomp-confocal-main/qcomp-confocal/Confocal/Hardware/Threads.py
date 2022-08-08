"""
Created on Apr 20, 2015
@author: Kai Zhang

Modified on Nov 4, 2019 for Python3 and Qt5 functionality
@Gurudev Dutt

Refactored the code and fixed minor errors on May 2, 2021
@Pubudu Wijesinghe
"""

from PyQt5 import QtCore
import time
import sys
import numpy


class CountThread(QtCore.QThread):

    """
    This thread is written for the ADWin counter
    It emits 1 signal: 'counts'
    Count Thread needs a hardware class as the parameter to initialize:
    ADWIN_MCL Class from the ADWIN_MCL library which has integrated functionality of ADwin and MCLND
    """

    SIGNAL_counts = QtCore.pyqtSignal(int, name='counts')

    def __init__(self, hardware, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.hardware = hardware
        self.counting = False

    def run(self):
        """
        This is being called by the Confocal Wrapper (cThread.start) and it starts the ADWin process.
        While the self.counting is True, it gets data from the ADWin with the rate specified until it gets a False.
        """
        self.counting = True

        self.adw = self.hardware.adw
        self.adw.Start_Process(1)  # Process 1 is TrialCounter.TB1

        self.rate = 1
        self.adw.Set_Processdelay(1, int(300000000/self.rate))
        while self.counting:
            data = self.adw.Get_Par(1)  # counter 1
            self.counts.emit(data*self.rate)
            time.sleep(0.1)
        self.adw.Stop_Process(1)

    def change_rate(self, rate):
        """
        Used to change the counting rate
        """
        self.adw.Set_Processdelay(1, int(300000000/rate))
        time.sleep(1.0/rate)
        self.rate = rate

    def stop_counting(self):
        """
        Once the Stop push button is pressed the Wrapper calls this function to stop the counting.
        """
        # add codes
        # reset adwin counting rate to 1
        self.adw.Set_Processdelay(1, 300000000)
        self.counting = False


class PositionThread(QtCore.QThread):
    """
    This thread is written to Handle the position of the MCLND
    It emits 1 signal: 'done'
    Count Thread needs a hardware class as the parameter to initialize:
    ADWIN_MCL Class from the ADWIN_MCL library which has integrated functionality of ADwin and MCLND
    """

    SIGNAL_done = QtCore.pyqtSignal(float, float, float, name='done')

    def __init__(self, hardware, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.hardware = hardware
        self.command = []
        self.accuracy = 0.01

    def run(self):
        if len(self.command) != 3:
            sys.stderr.write('Error: No Command Position.')
            return
        else:
            self.nd = self.hardware.nd
            handle = self.hardware.nd_handle

            x_position = self.nd.SingleReadN('x', handle)
            x = self.command[0]
            success_flag = False
            while not success_flag:
                i = 0
                while abs(x_position - x) > self.accuracy:
                    x_position = self.nd.MonitorN(x - self.hardware.nd_dx, 'x', handle)
                    i += 1
                    time.sleep(0.01)
                    if i == 50:
                        self.hardware.nd_dx = x_position - x
                        break
                success_flag = True

            y_position = self.nd.SingleReadN('y', handle)
            y = self.command[1]
            success_flag = False
            while not success_flag:
                i = 0
                while abs(y_position - y) > self.accuracy:
                    y_position = self.nd.MonitorN(y - self.hardware.nd_dy, 'y', handle)
                    i += 1
                    time.sleep(0.01)
                    if i == 50:
                        self.hardware.nd_dy = y_position - y
                        break
                success_flag = True

            z_position = self.nd.SingleReadN('z', handle)
            z = self.command[2]
            success_flag = False
            while not success_flag:
                i = 0
                while abs(z_position - z) > self.accuracy:
                    z_position = self.nd.MonitorN(z - self.hardware.nd_dz, 'z', handle)
                    i += 1
                    time.sleep(0.01)
                    if i == 50:
                        self.hardware.nd_dz = z_position - z
                        break
                success_flag = True

            self.done.emit(x_position, y_position, z_position)


class ScanThread(QtCore.QThread):

    SIGNAL_init = QtCore.pyqtSignal(numpy.ndarray, name='init_image')
    SIGNAL_update = QtCore.pyqtSignal(numpy.ndarray, name='update_image')

    def __init__(self, hardware, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.hardware = hardware
        self.parameters = ()
        self.scanning = False
        self.accuracy = 0.01  # (micron) used in go_to function
        self.Actual = None

    def run(self):
        self.Actual = None
        if self.parameters == ():
            sys.stderr.write('No Scanning Parameters!')
            return -1
        self.scanning = True
        self.adw = self.hardware.adw
        self.nd = self.hardware.nd
        self.nd_handle = self.hardware.nd_handle

        self.init_data()
        self.init_image.emit(self.C)

        t1 = time.perf_counter()

        for x in self.xArr:
            try:
                self.go_to(x, self.yArr[0], self.z)
            except TypeError:
                self.hardware.nd_dx = 0
                self.hardware.nd_dy = 0
                self.go_to(x, self.yArr[0], self.z)

            self.adw.Start_Process(2)  # Process 2 is 1D_Scan.TB2

            #self.nd.ResetClocks(self.nd_handle)

            self.nd.ReadWaveFormNSetup('y', len(self.yArr)+20, self.nd_handle, rateMode=6)  # 6 for 500Hz freq
            self.nd.LoadWaveFormNSetup('y', len(self.yArr), self.yArr, self.nd_handle,rate=2)  # 2 ms rate
            yData = self.nd.WaveFormNTrigger('y', len(self.yArr)+20, self.nd_handle)  # Generates len(array)+20 pulses
            #print yData
            if len(yData) == len(self.yArr) + 20:
                countData = self.adw.GetData_Long(1, 1, len(self.yArr)+19)
                # The 1st pulse doesn't have counts. len(array) + 19 counts data.

            self.adw.Stop_Process(2)

            yData_new = (numpy.array(yData[:-1]) + numpy.array(yData[1:]))/2.0
            countData_new = numpy.asarray(countData)*self.freq
            #print yData_new
            self.dataHandle(x, yData_new, countData_new)

            if not self.scanning:
                return

            t2 = time.perf_counter()

            if t2-t1 > 1:
                self.update_image.emit(self.C)
                t1 = t2

        self.scanning = False

    def go_to(self, x, y, z):
        handle = self.nd_handle

        x_position = self.nd.SingleReadN('x', handle)
        success_flag = False
        while not success_flag:
            i = 0
            while abs(x_position - x) > self.accuracy:
                x_position = self.nd.MonitorN(x - self.hardware.nd_dx, 'x', handle)
                i += 1
                time.sleep(0.01)
                if i == 50:
                    self.hardware.nd_dx = x_position - x
                    break
            success_flag = True

        y_position = self.nd.SingleReadN('y', handle)
        success_flag = False
        while not success_flag:
            i = 0
            while abs(y_position - y) > self.accuracy:
                y_position = self.nd.MonitorN(y - self.hardware.nd_dy, 'y', handle)
                i += 1
                time.sleep(0.01)
                if i == 50:
                    self.hardware.nd_dy = y_position - y
                    break
            success_flag = True

        z_position = self.nd.SingleReadN('z', handle)
        success_flag = False
        while not success_flag:
            i = 0
            while abs(z_position - z) > self.accuracy:
                z_position = self.nd.MonitorN(z - self.hardware.nd_dz, 'z', handle)
                i += 1
                time.sleep(0.01)
                if i == 50:
                    self.hardware.nd_dz = z_position - z
                    break
            success_flag = True

    def init_data(self):
        xMin, xMax, xStep, yMin, yMax, yStep, self.z, self.freq = self.parameters
        if xStep > 0.05:
            self.accuracy = xStep/5
        if xMin == 0:
            self.hardware.nd_dx = 0
        if yMin == 0:
            self.hardware.nd_dy=0
        self.xArr = numpy.arange(xMin, xMax, xStep)
        self.yArr = numpy.arange(yMin, yMax, yStep)
        if len(self.xArr) != len(self.yArr):
            if len(self.xArr) - len(self.yArr) == 1:
                self.xArr = self.xArr[:-1]
            elif len(self.yArr) - len(self.xArr) == 1:
                self.yArr = self.yArr[:-1]
            else:
                sys.stderr.write('Square image only!')

        self.C = numpy.zeros((len(self.xArr), len(self.yArr)), int)

    def dataHandle(self, x, yData, countData):
        # create count data in a column
        pickCounts = []
        for each_y in self.yArr:
            # search yData to find the closest value
            each_yArr = numpy.array([each_y]*len(yData))
            diff = list(numpy.absolute(yData-each_yArr))
            i = diff.index(min(diff))
            pickCounts.append(countData[i])

        # find which column it is
        ix = list(self.xArr).index(x)

        # put it into the C
        CT = list(numpy.transpose(self.C))
        CT[ix] = pickCounts
        self.C = numpy.transpose(numpy.asarray(CT))

        #print pickCounts
        # save the actual data (for future use)
        l = [x]*len(yData)
        line_actual = numpy.transpose(numpy.asarray([l, yData, countData]))
        if self.Actual is None:
            self.Actual = line_actual
        else:
            self.Actual = numpy.append(self.Actual, line_actual, axis=0)


class MaxThread(QtCore.QThread):

    SIGNAL_counts = QtCore.pyqtSignal(int, name='counts')

    def __init__(self, hardware, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.hardware = hardware
        self.command = []
        self.accuracy = 0.01
        self.maximizing = False

    def run(self):
        self.maximizing = True
        self.adw = self.hardware.adw
        self.nd = self.hardware.nd
        self.handle = self.hardware.nd_handle

        self.axis = 'x'
        self.offset = self.hardware.nd_dx
        self.scan()
        self.axis = 'y'
        self.offset = self.hardware.nd_dy
        self.scan()
        self.axis = 'z'
        self.offset = self.hardware.nd_dz
        self.scan()

        self.maximizing = False

    def go(self, command):
        position = self.nd.SingleReadN(self.axis, self.handle)

        success_flag = False
        while not success_flag:
            i = 0
            while abs(position-command) > self.accuracy:
                print(f'moving to {command} from {position}')
                position = self.nd.MonitorN(command - self.offset, self.axis, self.handle)
                i += 1
                time.sleep(0.01)
                if i == 50:
                    self.offset = position-command
                    break
            success_flag = True

    def count(self):
        rate = 1
        self.adw.Set_Processdelay(1, int(300000000/rate))
        self.adw.Start_Process(1)
        time.sleep(1.01/rate + 0.1)
        counts = self.adw.Get_Par(1)*rate
        self.adw.Stop_Process(1)
        return counts

    def scan(self, ran=0.5, step=0.05):
        positionList = []
        position = self.nd.SingleReadN(self.axis, self.handle)

        print('read position done.')

        counts_data = []
        p = position-ran/2
        while p <= position + ran/2:
            positionList.append(p)
            p += step
        for each_position in positionList:
            self.go(each_position)
            data = self.count()
            self.counts.emit(data)
            counts_data.append(data)

        self.go(positionList[counts_data.index(max(counts_data))])


class KeepThread(QtCore.QThread):

    SIGNAL_done=QtCore.pyqtSignal(int, name='done')

    def __init__(self, parent=None):
        QtCore.QThread.__init__(self,parent)
        self.parent = parent
        self.running = False

    def run(self):
        self.running=True
        self.parent.ui.pbMax.click()
        print('Maximizing...', end=' ')
        time.sleep(2)
        while not self.parent.ui.pbCount.isEnabled():
            time.sleep(2)
        print('Done.')
        self.parent.ui.pbCount.click()
        print('Counting...', end=' ')
        time.sleep(5)
        max_count=self.parent.ui.lcdNumber.intValue()
        time.sleep(5)
        while self.running:
            count = self.parent.ui.lcdNumber.intValue()
            if count == max_count:
                self.parent.ui.pbCount.click()
                time.sleep(1)
                self.parent.ui.pbCount.click()
                time.sleep(1.1)
                count = self.parent.ui.lcdNumber.intValue()
            if float(count)/max_count < 0.7:
                print(count, max_count, 'Needs tracking!')
                self.parent.ui.pbCount.click()
                time.sleep(2)
                self.parent.ui.pbMax.click()
                print('Maxing...', end=' ')
                time.sleep(2)
                while not self.parent.ui.pbCount.isEnabled():
                    time.sleep(2)
                print('Done.')
                print('Record position:'+str(self.parent.ui.txtX.text())+','+str(self.parent.ui.txtY.text())+','+str(self.parent.ui.txtZ.text()))
                self.parent.ui.pbCount.click()
                print('Counting...')
                time.sleep(5)
                max_count = self.parent.ui.lcdNumber.intValue()