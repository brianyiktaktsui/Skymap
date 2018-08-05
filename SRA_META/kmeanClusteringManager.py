#
__author__ = 'btsui'

import kmeanOnto
import inputPartitionerKmean
from clusterBaseClass import  clusterBaseClass
import mergeKmeanResults as Merger
import os
class kmeanClusteringMangaer(clusterBaseClass):
    className='kmeanClusteringMangaer'

    def __init__(self):
        clusterBaseClass.__init__(self,
                                  outputPostfix=kmeanOnto.outputPostfix,
                                  baseSplitDir='/cellar/users/btsui/Data/nrnb01_nobackup/tmp/METAMAP//splittedInput_'+self.className+'_',
                                  pythonScriptName='/cellar/users/btsui/Project/METAMAP/code/metamap/kmeanOnto.py',
                                  CWD='/cellar/users/btsui/Project/METAMAP/code/metamap',
                                  minCorrectSize=0,
                                  memory=2,
                                  smp=4
                                  )
    def run(self,inputFDir,srrToCUIDir,outDir):
        #consist of both input for clustering
        fname=inputFDir.split('/')[-1]
        self.splitOutDir=self.baseSplitDir+fname+'/' 
        print 'splitting input'
        LS=inputPartitionerKmean.inputPartitionerKmean()#[MOD]CHANGE
        termToId=LS.split(inputFDir,self.nFiles,self.splitOutDir,srrToCUIDir,clean=True)#retain signature
        self.setNFiles(len(termToId))
        if not self.Done():
            #fname,nfiles,splitOutDir
            self.processUntilAllDone()
        Merger.runMerger(inputFDir,self.splitOutDir,outDir=outDir)
if __name__=='__main__':
    #'.realign.spliceVariantMaxMatrix'
    
    geneBySampleFDir='/cellar/users/btsui/Data/nrnb01_nobackup/Data/SRA/MATRIX/DATA/hgGRC38/allSRAmatrix.realign.gene.bin'#+'.spliceVariantMaxMatrix'
    #geneBySampleFDir='/oasis/btsui/Data/SRA/MATRIX/DATA/hgGRC38/allSRAspliceVariantMaxMatrix'
    srrToCUIDir='/cellar/users/btsui/Data/nrnb01_nobackup/METAMAP/srrToNCI.pyc.attrib.embryo.test.t.0.3'
    srrToCUIFname=srrToCUIDir.split('/')[-1]
    outDir='/cellar/users/btsui/Data/nrnb01_nobackup/METAMAP/'+'kmean_'+srrToCUIFname+'/'
    if not os.path.exists(outDir):
        os.makedirs(outDir)
    print outDir
    m=kmeanClusteringMangaer()
    m.run(geneBySampleFDir,srrToCUIDir=srrToCUIDir,outDir=outDir)
