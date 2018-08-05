#
__author__ = 'btsui'
from inputPartitionerText import inputPartitionerText
import os
from metamapping import Metamap
import time
import subprocess as sp
from clusterBaseClass import  clusterBaseClass
class metamappingManager(clusterBaseClass):

    def __init__(self):
        clusterBaseClass.__init__(self,
                                  outputPostfix=Metamap.outputPostfix,
                                  baseSplitDir='/cellar/users/btsui/Data/nrnb01_nobackup/METAMAP/splittedInput_',
                                  pythonScriptName='/cellar/users/btsui/Project/METAMAP/code/metamap/metamapping.py',
                                  CWD='/cellar/users/btsui/Project/METAMAP/code/metamap',
                                  minCorrectSize=5000
                                  )
    def run(self,inputFDir):
        fname=inputFDir.split('/')[-1]

        self.splitOutDir=self.baseSplitDir+fname+'/'
        os.system('rm -r '+self.splitOutDir)
        if not self.Done():
            LS=inputPartitionerText()
            #fname,nfiles,splitOutDir
            print 'splitting input'
            splittedFiles=LS.split(inputFDir,self.nFiles,self.splitOutDir,clean=self.TEST)
            self.processUntilAllDone()

if __name__=='__main__':
    fname='/cellar/users/btsui/Data/nrnb01_nobackup/METAMAP/input/test.out'
    m=metamappingManager()
    m.run(fname)
[]