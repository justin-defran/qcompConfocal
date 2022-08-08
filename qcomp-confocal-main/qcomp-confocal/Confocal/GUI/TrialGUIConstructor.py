'''
Created on Jul 7, 2015

@author: Kai Zhang
'''
import subprocess
subprocess.call(['pyuic4','GUI.ui','>','GUI.py'],shell=True)
