from Hardware.ADWIN_MCL import ADWIN_MCL
import sys,time,numpy
import matplotlib.pylab as plt
import numpy as np


hardware=ADWIN_MCL()
hardware.initialize()
adw = hardware.adw
nd = hardware.nd

handle = hardware.nd_handle

xposition = nd.SingleReadN('x', handle)

print xposition