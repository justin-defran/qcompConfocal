#from Hardware.Threads import CountThread,PositionThread,ScanThread,MaxThread,KeepThread
from Hardware.ADWIN_MCL import ADWIN_MCL
import sys,time,numpy
import matplotlib.pylab as plt
import numpy as np


hardware=ADWIN_MCL()
hardware.initialize()
adw = hardware.adw
nd = hardware.nd
'''

sThread = ScanThread(hardware)
sThread.parameters=(0.0,100.0,1.0,0.0,100.0,1.0,59.0,500.0)
sThread.start()
'''


def go_to(x, y, z):
    handle = hardware.nd_handle
    accuracy = 0.01
    xposition = nd.SingleReadN('x', handle)
    success_flag = False
    while not success_flag:
        i = 0
        while abs(xposition - x) > accuracy:
            xposition = nd.MonitorN(x - hardware.nd_dx, 'x', handle)
            i += 1
            time.sleep(0.01)
            if i == 50:
                hardware.nd_dx = xposition - x
                break
        success_flag = True

    yposition = nd.SingleReadN('y', handle)
    success_flag = False
    while not success_flag:
        i = 0
        while abs(yposition - y) > accuracy:
            yposition = nd.MonitorN(y - hardware.nd_dy, 'y', handle)
            i += 1
            time.sleep(0.01)
            if i == 50:
                hardware.nd_dy = yposition - y
                break
        success_flag = True

    zposition = nd.SingleReadN('z', handle)
    success_flag = False
    while not success_flag:
        i = 0
        while abs(zposition - z) > accuracy:
            zposition = nd.MonitorN(z - hardware.nd_dz, 'z', handle)
            i += 1
            time.sleep(0.01)
            if i == 50:
                hardware.nd_dz = zposition - z
                break
        success_flag = True
'''
def dataHandle(x, yData, countData):
    # create count data in a column
    pickCounts = []
    for each_y in yArr:
        # search yData to find the closest value
        each_yArr = numpy.array([each_y] * len(yData))
        diff = list(numpy.absolute(yData - each_yArr))
        i = diff.index(min(diff))
        pickCounts.append(countData[i])

    # find which column it is
    ix = list(xArr).index(x)

    # put it into the C
    CT = list(numpy.transpose(C))
    CT[ix] = pickCounts
    C = numpy.transpose(numpy.asarray(CT))

    # save the actual data (for future use)
    l = [x] * len(yData)
    line_actual = numpy.transpose(numpy.asarray([l, yData, countData]))
    if Actual is None:
        Actual = line_actual
    else:
        Actual = numpy.append(Actual, line_actual, axis=0)
'''
def run(xArr,yArr,z,freq):
    nd_handle = hardware.nd_handle
    C = numpy.zeros((len(xArr), len(yArr)), int)
    for x in xArr:
        try:
            go_to(x, yArr[0], z)
        except TypeError:
            hardware.nd_dx = 0
            hardware.nd_dy = 0
            go_to(x, yArr[0], z)

        adw.Start_Process(2)

        # self.nd.ResetClocks(self.nd_handle)
        nd.ReadWaveFormNSetup('y', len(yArr) + 20, nd_handle, rateMode=6)  # 6 for 500Hz freq
        nd.LoadWaveFormNSetup('y', len(yArr), yArr, nd_handle, rate=2)  # 2 ms rate
        yData = nd.WaveFormNTrigger('y', len(yArr) + 20, nd_handle)  # Generates len(array)+20 pulses

        if len(yData) == len(yArr) + 20:
            countData = adw.GetData_Long(1, 1, len(yArr) + 19)  # The 1st pulse doesn't have counts. len(array)+19 counts data.

        adw.Stop_Process(2)

        yData_new = (numpy.array(yData[:-1]) + numpy.array(yData[1:])) / 2.0
        #print yData_new
        countData_new = numpy.asarray(countData) * freq


        # create count data in a column
        pickCounts = []
        for each_y in yArr:
            # search yData to find the closest value
            each_yArr = numpy.array([each_y] * len(yData_new))
            diff = list(numpy.absolute(yData_new - each_yArr))
            i = diff.index(min(diff))
            pickCounts.append(countData_new[i])

        # find which column it is
        ix = list(xArr).index(x)
        #print pickCounts
        # put it into the C
        CT= list(numpy.transpose(C))
        CT[ix] = pickCounts
        C = numpy.transpose(numpy.asarray(CT))
        #print x

    return C


xMin=1.0
xMax=99.0
xStep=0.2

yMin=1.0
yMax=99.0
yStep=0.2

x=numpy.arange(xMin,xMax,xStep)
y=numpy.arange(yMin,yMax,yStep)
z=54.9
freq=500
z_list= np.arange(54.9,44.9,-1.0)

print z_list


for z in z_list:
    Counts=run(x,y,z,freq)
    plt.savetxt("D:\workspace\Data\confocal\\2019-05-02\\" + str(z) + "counts.txt",Counts)


    im=plt.imshow(Counts,origin='lower',extent=[min(x), max(x), min(y), max(y)])
    cb=plt.colorbar()
    #plt.show()
    plt.savefig("D:\workspace\Data\confocal\\2019-05-02\\"+str(z)+".png")
    plt.close()
    print z






