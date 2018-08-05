__author__ = 'btsui'
from inputPartitionerText import inputPartitionerText
import os
from metamapping import Metamap
import time
import subprocess as sp
from clusterBaseClass import  clusterBaseClass
from  MetamapParser import MetamapParse
class metamappingParsingManager(clusterBaseClass):

    def __init__(self):
        clusterBaseClass.__init__(self,
                                  outputPostfix=MetamapParse.outputPostfix,
                                  baseSplitDir='/cellar/users/btsui/Data/nrnb01_nobackup/METAMAP/splittedInput_',
                                  pythonScriptName='/cellar/users/btsui/Project/METAMAP/code/metamap/MetamapParser.py',
                                  CWD='/cellar/users/btsui/Project/METAMAP/code/metamap',
                                  minCorrectSize=1
                                  )
    def run(self,inputFDir):
        fname=inputFDir.split('/')[-1]
        self.splitOutDir=self.baseSplitDir+fname+'/'
        splittedFiles=self.returnFiles()
        if not self.Done():
            self.processUntilAllDone()
