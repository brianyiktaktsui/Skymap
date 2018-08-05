__author__ = 'btsui'
from collections import defaultdict
import os
import pandas as pd
import sharedVariable as sh
class inputPartitionerKmean:
    """
    input: file name, nfiles
    output: file names of the splitted files

    design:
        assign the file based on the value of (position mod nfiles)
    """
    termToIdSDir='.termToId.pyc'
    def split(self,fname,nfiles,splitOutDir,srrToCUIDir,clean=True,minN=3):


        if not os.path.isdir(splitOutDir):
            os.makedirs(splitOutDir)
        if clean:
            self.cleanDir(splitOutDir)
        #load transcript DF
        trscrptBySrr=sh.loadDf(fname)
        tmpSrrToTerms=pd.read_pickle(srrToCUIDir)
        srrToTerms=tmpSrrToTerms[tmpSrrToTerms.index.isin(trscrptBySrr.columns)]
        #find the Term to Sample Dict
        termToSrrDict=defaultdict(set)
        for srr,term in srrToTerms.iteritems():
            termToSrrDict[term].add(srr)
        #parition the term and sample to files

        filteredDict={ term:SRRset for term,SRRset in termToSrrDict.iteritems() if len(SRRset)>=sh.maxNClusters}
        #keep a table of term to ID
        termToId= pd.Series(range(1,len(filteredDict.keys())+1),index=filteredDict.keys())
        termToId.to_pickle(self.termToIdSDir)
        #read in trnascriptome DF

        print trscrptBySrr.shape
        for term,i in termToId.iteritems():
            srrSet=filteredDict[term]

            subDF=trscrptBySrr.loc[:,trscrptBySrr.columns.isin(srrSet) ]
            sh.exportDf(splitOutDir+str(i),subDF)
        #spit the key file into different files
        return termToId


    def cleanDir(self,splitOutDir):
        print 'cleaning \n\n'
        #print 'rm '+splitOutDir+'/*'

        os.system('rm '+splitOutDir+'/*')
        #map(lambda fname:os.remove(splitOutDir+fname) ,os.listdir(splitOutDir))

if __name__=='__main__':
    LS=inputPartitionerKmean()
    splitOutDir='/cellar/users/btsui/Data/nrnb01_nobackup/METAMAP/splittedInput/'
    #LS.cleanDir(splitOutDir)
    geneBySampleFDir='/oasis/btsui/Data/SRA/MATRIX/DATA/hgGRC38/allSRAspliceVariantMaxMatrix'
    srrToCUIDir='/cellar/users/btsui/Data/nrnb01_nobackup/METAMAP/srrToCUI.pyc.attrib.nonsyn'
    LS.split(geneBySampleFDir,2,splitOutDir,srrToCUIDir ,clean=True)
