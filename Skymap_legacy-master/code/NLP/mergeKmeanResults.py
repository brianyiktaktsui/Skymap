__author__ = 'btsui'
import sharedVariable as shv
import os
import pandas as pd
import inputPartitionerKmean
from NCITerminology import NCITerminology
def returnFilesNamesWithExtd(labelExtd,inDir):
    listOfSFnames=filter( lambda fname:fname.endswith(labelExtd), os.listdir(inDir))
    listOfFullDir=map(lambda fname:inDir+fname,listOfSFnames)
    return listOfFullDir
def extractIdFromFDir(Dir):
    return int(Dir.split('/')[-1].split('.')[0])
def mergeMemershipsSeries(inDir):
    """
    inDir:
    :return: a combined series of data
    """
    labelExtd='.label.pyc'
    listOfFullDir=returnFilesNamesWithExtd(labelExtd,inDir)
    termIdToLabelSDict={extractIdFromFDir(dir):dir for dir in listOfFullDir}
    listOfEncodedS=[i*shv.maxNClusters+pd.read_pickle(dir) for i,dir in termIdToLabelSDict.iteritems() ]
    return pd.concat(listOfEncodedS)

def mergeControidsDF(inDir):
    """
    #unfinished
    :param inDir:
    :return:
    """
    #

    #get centroidfiles
    labelExtd='.centroid.pyc'

    listOfFullDir=returnFilesNamesWithExtd(labelExtd,inDir)
    termIdToCentroidsDFDict={extractIdFromFDir(Dir):pd.read_pickle(Dir) for Dir in  listOfFullDir}
    #get label Dict
    labelExtd='.label.pyc'
    listOfFullDir=returnFilesNamesWithExtd(labelExtd,inDir)
    termIdToLabelSDict={extractIdFromFDir(dir):pd.read_pickle(dir) for dir in listOfFullDir}

    #get variance Dict

    ###for Ids
    myTermToIdSDir=inputPartitionerKmean.inputPartitionerKmean.termToIdSDir
    cellIdToFileIndexS=pd.read_pickle(myTermToIdSDir)
    FileIndexToCellId={Index:cellId for cellId ,Index in cellIdToFileIndexS.iteritems()}
    keyMax=max(termIdToCentroidsDFDict.keys())
    profileIdToCellIds=pd.Series(index= range((keyMax+1)*shv.maxNClusters))
    mergedMemberShipS=pd.Series()
    for i, DF in termIdToCentroidsDFDict.iteritems():
        DF.index=i*shv.maxNClusters+DF.index
        profileIdToCellIds[DF.index]=FileIndexToCellId[i]
        LabelS=termIdToLabelSDict[i]
        labelSToCentroidS=LabelS+i*shv.maxNClusters
        mergedMemberShipS=mergedMemberShipS.append(labelSToCentroidS)
        #i: nThCentroid, DF.index: the centroid id, each centroid id should inherit the nThCentroid Label
    return pd.concat(termIdToCentroidsDFDict.values()),profileIdToCellIds,mergedMemberShipS
def getColumnsAnnotations(dfDir):
    with open(dfDir+'.column.txt') as f:
        return f.read().split('\n')
def runMerger(geneBySampleFDir,inDir,outDir):
    fname=geneBySampleFDir.split('/')[-1]
    membershipSName=outDir+fname+'.kmeanMembership.merged.pyc'
    membershipCentroidsName=outDir+fname+'.kmeanCentroids.merged.pyc'
    centroidIdToOntoSName=outDir+fname+'.centroidIdToOntoS.merged.pyc'
    centroidIdToEngSName= outDir+fname+'.centroidIdToEngS.merged.pyc'
    #mergedS=mergeMemershipsSeries(inDir)

    mergedCentroidsDF,centroidIdToOntoS,mergedMemberShipS=mergeControidsDF(inDir)
    mergedMemberShipS.to_pickle(membershipSName)
    annotations=getColumnsAnnotations(geneBySampleFDir)
    mergedCentroidsDF.columns=annotations
    mergedCentroidsDF.to_pickle( (membershipCentroidsName) )
    #centroidIdToOntoS=generateCentroidIdToOntoIdConvertionS(mergedCentroidsDF)
    centroidIdToOntoS.to_pickle(centroidIdToOntoSName)

    onto=NCITerminology()
    centroidIdToOntoSNonNa=centroidIdToOntoS.dropna()
    centroidIdToEngS=pd.Series(onto.cleanedIdS[centroidIdToOntoSNonNa.values].values,index=centroidIdToOntoSNonNa.index)
    centroidIdToEngS.to_pickle(centroidIdToEngSName)
if __name__=='__main__':
    geneBySampleFDir='/oasis/btsui/Data/SRA/MATRIX/DATA/hgGRC38/allSRAspliceVariantMaxMatrix'
    dfName=geneBySampleFDir.split('/')[-1]

    inDir='/oasis/btsui/tmp/METAMAP/splittedInput_kmeanClusteringMangaer_'+dfName+'/'
    print inDir
    outDir='/cellar/users/btsui/Data/nrnb01_nobackup/METAMAP/'
    runMerger(geneBySampleFDir,inDir,outDir)
    """
    membershipSName='kmeanMembership.merged.pyc'
    membershipCentroidsName='kmeanCentroids.merged.pyc'
    centroidIdToOntoSName='centroidIdToOntoS.merged.pyc'
    mergedS=mergeMemershipsSeries(inDir)
    mergedS.to_pickle(outDir+membershipSName)
    mergedCentroidsDF=mergeControidsDF(inDir)
    annotations=getColumnsAnnotations(geneBySampleFDir)
    mergedCentroidsDF.columns=annotations
    mergedCentroidsDF.to_pickle( (outDir+membershipCentroidsName) )
    centroidIdToOntoS=generateCentroidIdToOntoIdConvertionS(mergedCentroidsDF)
    centroidIdToOntoS.to_pickle(outDir+centroidIdToOntoSName)
    """