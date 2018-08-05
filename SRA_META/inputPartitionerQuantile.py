__author__ = 'btsui'
__author__ = 'btsui'
from collections import defaultdict
import os
import pandas as pd
import sharedVariable as sh
class inputPartitionerQuantile:
    """
    input: file name, nfiles
    output: file names of the splitted files

    design:
        assign the file based on the value of (position mod nfiles)
    """
    termToIdSDir='.termToId.pyc'
    def split(self,fname,nfiles,splitOutDir,clean=True):


        if not os.path.isdir(splitOutDir):
            os.mkdir(splitOutDir)
        if clean:
            self.cleanDir(splitOutDir)
        trscrptBySrr=sh.loadDf(fname)
        chunkSize=trscrptBySrr.shape[1]/nfiles
        print 'chunkSize: ',chunkSize
        for i in range(nfiles):
            DFindex= i*chunkSize
            lastIndex=(nfiles-1)
            ub= trscrptBySrr.shape[1] if i==lastIndex else DFindex+chunkSize
            subDF=trscrptBySrr.iloc[:,DFindex:ub ]
            sh.exportDf(splitOutDir+str(i+1),subDF)

        #spit the key file into different files



    def cleanDir(self,splitOutDir):
        print 'cleaning \n\n'
        map(lambda fname:os.remove(splitOutDir+fname) ,os.listdir(splitOutDir))

