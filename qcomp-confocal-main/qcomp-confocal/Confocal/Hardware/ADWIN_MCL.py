'''
Created on Apr 20, 2015

@author: Duttlab8
'''
from .MCL.NanoDrive import MCL_NanoDrive # import statement fixed - Gurudev Nov. 4, 2019
import ADwin
import sys,os,time


class ADWIN_MCL():
    '''
    This is for ADWIN_MCL confocal setup.
    '''


    def __init__(self,*args):
        pass

    def initialize(self):
        '''
        Return value is 0 if OK, -1 if not OK

        '''
        self.nd=MCL_NanoDrive()
        self.nd_handle=self.nd.InitHandles().get('L')
        if self.nd_handle==None:
            return -1
        self.nd_dx=0
        self.nd_dy=0
        self.nd_dz=0
        
        self.adw=ADwin.ADwin()
        if self.adw_boot():
            if self.adw_load_process():
                return 0

        return -1
    
    def adw_boot(self):
        try:
            btl = self.adw.ADwindir + 'ADwin11.btl'
            self.adw.Boot(btl)
            return True
        except ADwin.ADwinError as e:
            sys.stderr.write(e.errorText)
            return False
            
    def adw_load_process(self):
        try:
            count_proc = os.path.join(os.path.dirname(__file__),'ADWIN\\TrialCounter.TB1') # as p TrialCounter is configuredrocess 1 TrialCounter
            self.adw.Load_Process(count_proc)
            oned_scan_proc = os.path.join(os.path.dirname(__file__),'ADWIN\\1D_Scan.TB2') # 1D_Scan is configured as process 2
            self.adw.Load_Process(oned_scan_proc)
            return True
        except ADwin.ADwinError as e:
            sys.stderr.write(e.errorText)
            return False
        
    def laser_on(self):
        self.nd.SetClock('Aux', 1, self.nd_handle)
        
    def laser_off(self):
        self.nd.SetClock('Aux', 0, self.nd_handle)
        
    # TODO: Really need to add more methods to this class such as getting adwin data, going to a position in ND
    # TODO: there should be 2 classes, one for Adwin and one for MCL
    def cleanup(self):
        
        self.nd.ReleaseAllHandles()
        
        self.adw.Clear_Process(1)
        self.adw.Clear_Process(2)
        return 0

