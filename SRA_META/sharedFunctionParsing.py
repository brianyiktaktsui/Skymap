__author__ = 'btsui'
import pandas as pd
from sharedVariable import *
import pandas as pd
from collections import defaultdict

CWD='/cellar/users/btsui/Project/CancerSpliceIsoform/GTEx/parseBioSample/'
nci_csv_file_dir='/cellar/users/btsui/Project/CancerSpliceIsoform/GEO/DATA_PROCESSING/IpythonNotebook/NCIT.csv'
idConvertionTable=CWD+"sraQueryOutput.txt"
inputFile=CWD+'allBioSample.transcriptome.mouse.human.doublespace.csv.merged.out'
outFName='/cellar/users/btsui/Data/nrnb01_nobackup/GEO_META/GSMToNCIDFPickle'
NCIGraph='/cellar/users/btsui/Project/CancerSpliceIsoform/GEO/DATA_PROCESSING/IpythonNotebook/NCITerminology.enriched.pyc'
srrToTermDFDir='/cellar/users/btsui/Data/nrnb01_nobackup/Data/SRA/MATRIX/biosample/SraToNCIDFPickle'
umlsToNCI=None
NCIIdSet=None
biosampleToSrrDict=None



#get biosample to list of SRR dict

def _init():
    global umlsToNCI
    global NCIIdSet
    global biosampleToSrrDict
    nci_csv=pd.DataFrame.from_csv(nci_csv_file_dir)
    tmpDf=nci_csv.loc[:,['code','UMLS_CUI']].dropna().drop_duplicates(subset=['UMLS_CUI'])
    umlsToNCI=pd.Series(tmpDf.code.values, index=tmpDf.UMLS_CUI)
    NCIIdSet=set(nci_csv.UMLS_CUI.unique().tolist())

    biosampleToSrrDict=getBiosampleToSrrDict(genomeBuild,baseDirDict)

def parseRecordsToDictUMLS(inputFile):
    index=0
    with open(inputFile)as rf:
            myDict={}
            biosampleId=None
            seenForRecord={}
            for l in rf:
                if 'Processing 00000000.tx.1:' in l :
                    if ',' in l.split(': ')[1]:
                        potentialId=l.split(': ')[1].split(',')[0]
                            #flush previous term if there is any
                        if biosampleId!=None:
                            myDict[biosampleId]=seenForRecord
                        #refresh seen term
                        biosampleId= potentialId
                        seenForRecord={}
                        if index%100==0:
                            print index
                        index+=1

                if ':' in l:
                    firstHalf=l.split(':')[0]
                    firstHalfPeices=filter(lambda c:c!='',firstHalf.split(' '))
                    potentialId=firstHalfPeices[-1]

                    if potentialId[0]=='C' and (potentialId not in seenForRecord):
                        score=firstHalfPeices[0]

                        seenForRecord[potentialId]=int(score)
    return myDict
def getBiosampleToSrrDict(genomeBuild,baseDirDict):
    biosampleToSrrDict=defaultdict(set)
    for dtype, metaDir in baseDirDict.iteritems():
        for genome in genomeBuild:
            myS=pd.DataFrame.from_csv(metaDir+genome+'/metaData.txt').BioSample
            for srr,biosample in myS.iteritems():
                biosampleToSrrDict[biosample].add(srr)
    return biosampleToSrrDict

import numpy as np
import pandas as pd
def generateBiosampleMatrix(bioSampleToNciDict):
    allNci=set()
    for nciIds in  bioSampleToNciDict.itervalues():
        for nci in nciIds.keys():
            allNci.add(nci)
    listNCI=list(allNci)
    index,column=bioSampleToNciDict.keys(),listNCI
    bioSampleToNCIDF=pd.DataFrame(np.zeros( (len(index),len(column)) ) ,index=index,columns=column)
    index=0
    for bioSampleId,nciToScoreDict in bioSampleToNciDict.iteritems():
        #print nciToScoreDict.keys()
        bioSampleToNCIDF.loc[bioSampleId,nciToScoreDict.keys()]=nciToScoreDict.values()
        if index%1000==0:
            print index

        index+=1
    return bioSampleToNCIDF

AllBioSampleIds={genome+'_'+dtype:pd.DataFrame.from_csv(Dir+genome+'/metaData.txt').BioSample for genome in genomeBuild for dtype, Dir in baseDirDict.iteritems()}
srrToBioSampleS=pd.concat(AllBioSampleIds.values())

def upgradeToSRRMatrix(InputDF):
    biosampleToSRR=defaultdict(set)
    returnDF=createEmptyDf( srrToBioSampleS.index.unique(),InputDF.columns )
    for srr,biosample in srrToBioSampleS.iteritems():
        if biosample in InputDF.index:
            returnDF.loc[srr]=InputDF.loc[biosample]
    return returnDF
def fromFileToMatrix(fname):
    myDict=parseRecordsToDictUMLS(fname)
    return generateBiosampleMatrix(myDict)

def convertFileToUMLSDF(fname):
    tmpDF=fromFileToMatrix(fname)
    import metamapParam
    cellOntologySampleToUMLSDF=pd.DataFrame( tmpDF.as_matrix(),index=map(lambda s:s.replace(metamapParam.gibberish,''),tmpDF.index),columns=tmpDF.columns)
    exportDf(fname,cellOntologySampleToUMLSDF)

#####initialize the CUI
_init()
