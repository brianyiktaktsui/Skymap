__author__ = 'btsui'

__author__ = 'btsui'

import quantile
import inputPartitionerQuantile
from clusterBaseClass import  clusterBaseClass
import os
import pandas as pd
import sharedVariable as sh
class quantileMangaer(clusterBaseClass):
    className='quantileMangaer'
    def __init__(self):
        clusterBaseClass.__init__(self,
                                  outputPostfix=quantile.outputPostfix,
                                  baseSplitDir='/oasis/btsui/tmp/METAMAP//splittedInput_'+self.className+'_',
                                  pythonScriptName='/cellar/users/btsui/Project/METAMAP/code/metamap/quantile.py',
                                  CWD='/cellar/users/btsui/Project/METAMAP/code/metamap',
                                  minCorrectSize=0,
                                  memory=10,
                                  smp=1
                                  )
        self.setNFiles(100)
    def mergeFiles(self):
        files=[ sh.loadDf(self.splitOutDir+'/'+str(i)+ quantile.myPostfix).T for i in range(1,self.nFiles+1)]
        concatedFile=pd.concat(files)
        return concatedFile.T
    def run(self,inputFDir):
        #consist of both input for clustering
        fname=inputFDir.split('/')[-1]
        self.splitOutDir=self.baseSplitDir+fname+'/'
        print 'splitting input'
        #partiioaning files
        LS=inputPartitionerQuantile.inputPartitionerQuantile()#[MOD]CHANGE
        LS.split(inputFDir,self.nFiles,self.splitOutDir,clean=True)#retain signature

        if not self.Done():
            self.processUntilAllDone()
        outDf=self.mergeFiles()
        sh.exportDf(inputFDir+'.quant',outDf)
if __name__=='__main__':
    geneBySampleFDir='/oasis/btsui/Data/SRA/MATRIX/DATA/hgGRC38/TCGAmatrix'
    m=quantileMangaer()
    m.run(geneBySampleFDir)
