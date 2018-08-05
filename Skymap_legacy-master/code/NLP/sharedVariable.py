import pandas as pd
import numpy as np
import os
import shutil
Multithreading=True
from scipy.sparse import csr_matrix
idConvertionTable="/cellar/users/btsui/Project/CancerSpliceIsoform/GTEx/parseBioSample/sraQueryOutput.txt"
specie="mmGRC38"
specieEngDict={'hg':'Homo sapiens','mm':'Mus musculus'}
specieEng=specieEngDict[specie[:2]]
genomeBuild=['hgGRC38','mmGRC38'] #list of genome build
transcriptPrefixDict={"mmGRC38":'ENSMUST','hgGRC38':'ENST'}
transcriptPrefix=transcriptPrefixDict[specie]
kmeanPath='/oasis/btsui/Data/SRA/nci_kmean/'+specie+'/'
CWD=os.getcwd()+"/"
sampleSpace="allSRA"
dataMatrixDir="/oasis/btsui/Data/SRA/MATRIX/DATA/"
geneByTrascriptMatrix=dataMatrixDir+''
tcgaDataDir='/scratch/btsui/Data/TCGA_FROM_RAW/'


baseDirDict={'meth':'/cellar/users/btsui/Data/nrnb01_nobackup/METH/META_DATA/'
 ,'trans':'/cellar/users/btsui/Data/SRA/META/'
 }

"""
"""
baseMetaDataDir='/cellar/users/btsui/Data/nrnb01_nobackup/METAMAP/'

mergeCentroidMatrix='mergedCentroids'
mergeCentroidDir=dataMatrixDir+specie+'/'+mergeCentroidMatrix
maxNClusters=3
#dataMatrixDir="/cellar/users/btsui/Data/nrnb01_nobackup/Data/SRA/MATRIX/DATA/"
geneTranscriptVariantMatrixFileName = dataMatrixDir+specie+'/'+"geneByTranscriptVariantMatrix"

transcriptBySraDir=dataMatrixDir+specie+"/"+sampleSpace+"spliceVariantMaxMatrix"
TCGAtranscriptBySraDir=dataMatrixDir+specie+"/"+"TCGA"+"spliceVariantMaxMatrix"
#print "input:"
#print "transcriptBySraDir:\t",transcriptBySraDir
terminologyFName='NCITerminology.enriched.pyc'
denseNCISubGraphFname='denseSubGraph.gpickle'
CUIToNCIDFPickleFname="CUIToNCIDFPickle.pyc"
cuiVarSPickleFname=dataMatrixDir+specie+"/"+'cuiVarS.pyc'
biosampleMatrix="/oasis/btsui/Data/SRA/MATRIX/biosample/"
#biosampleMatrix="/cellar/users/btsui/Data/nrnb01_nobackup/Data/SRA/MATRIX/biosample/"
SRAToNCIDFPickleFname=biosampleMatrix+"SraToNCIDFPickle"
propagationExtd=".propagation"
#print "SRAToNCIDFPickleFname:\t",SRAToNCIDFPickleFname
#print "\n"
SRAToNCIDPropagatedFPickleFname=SRAToNCIDFPickleFname+propagationExtd
transcriptByTermExtension="TranscriptByTerm"
transcriptByTermDir=dataMatrixDir+specie+"/"+sampleSpace+transcriptByTermExtension

#output:
sraByTermScoreExtension="SraByTerm.log.score"
transcriptByTermScoreDir=dataMatrixDir+specie+"/"+sampleSpace+sraByTermScoreExtension
#print "output:"
#print "sraByTerm:\t",transcriptByTermDir
#%matplotlib inline
def runInRioja(bashLine):
    return os.system("ssh btsui@rioja.ucsd.edu "+bashLine)

def cuiToStrings(CUI):
    mysql_cn= MySQLdb.connect(host='avesso',
                    port=3306,user='btsui', passwd='password',
                    db='umls')
    return pd.read_sql("select * from MRCONSO where LAT='ENG' and ISPREF='Y' and CUI='"+CUI+"' limit 1", con=mysql_cn).iloc[0].STR
def nciIdToStrings(NCIId):
    mysql_cn= MySQLdb.connect(host='avesso',
                    port=3306,user='btsui', passwd='password',
                    db='umls')
    tmpDf=pd.read_sql("select * from MRCONSO where LAT='ENG' and SAB='NCI' and SCUI='"+NCIId+"' limit 1", con=mysql_cn)
    return tmpDf.iloc[0].STR if len(tmpDf.index)>0 else ""
def createEmptyDf(SraToPropagatedDfIndex,SraToPropagatedDfColumns):
    tmpEmptyMatrix=np.zeros((len(SraToPropagatedDfIndex),len(SraToPropagatedDfColumns)),dtype=np.float64)
    return pd.DataFrame(tmpEmptyMatrix,index=SraToPropagatedDfIndex,columns=SraToPropagatedDfColumns)

cahceDir = "/tmp/btsui/cache/"

def cacheLoad(file):
    if not os.path.exists(cahceDir):
        os.makedirs(cahceDir)
    cachingFileName = file.replace("/", "_")  # change delimiter
    if not os.path.exists(cahceDir + cachingFileName):
        print ("start caching:\t", file, "\tas:\t", cahceDir + cachingFileName)
        shutil.copy(file, cahceDir + cachingFileName)
        print ("done caching")
    else:
        print ("already cached:\t", file, "\tas:\t", cahceDir + cachingFileName)

# get the name of the file in cache
def cacheName(file):
    cachingFileName = file.replace("/", "_")
    return cahceDir + cachingFileName

def exportDf(fname,myDF):
    with open(fname+'.index.txt','w') as f:
        f.write("\n".join(myDF.index.values))
    with open(fname+'.columns.txt','w') as f:
        f.write("\n".join(myDF.columns))
    np.save(fname+".npy",myDF.as_matrix())

def loadDf(fname,mmap_mode='r'):
    with open(fname+'.index.txt') as f:
        myIndex=map(lambda s:s.replace("\n",""), f.readlines())
    with open(fname+'.columns.txt') as f:
        myColumns=map(lambda s:s.replace("\n",""), f.readlines())
    tmpMatrix=np.load(fname+".npy",mmap_mode=mmap_mode)
    tmpDf=pd.DataFrame(tmpMatrix,index=myIndex,columns=myColumns)
    tmpDf.columns.name='Run'
    return tmpDf
"""
def loadDf(fname):
    with open(fname+'.index.txt') as f:
        myIndex=map(lambda s:s.replace("\n",""), f.readlines())
    with open(fname+'.columns.txt') as f:
        myColumns=map(lambda s:s.replace("\n",""), f.readlines())
    cacheLoad(fname+".npy")
    tmpMatrix=np.load(cacheName(fname+".npy"))
    return pd.DataFrame(tmpMatrix,index=myIndex,columns=myColumns)
"""
def tabulationToMembershipMatrixFormat(myAttribDf,attribA,attribB,weightLabel=None):
    
    import networkx as nx
    edge_attr= [weightLabel]if weightLabel !=None else []
    tmpG=nx.from_pandas_dataframe(myAttribDf,source=attribA,target=attribB,edge_attr=edge_attr)
    attribAVals=myAttribDf[attribA].unique()
    attribBVals=myAttribDf[attribB].unique()
    myNodeList=attribAVals.tolist()+attribBVals.tolist()
    sparseMembershipM=nx.to_scipy_sparse_matrix(G=tmpG,nodelist=myNodeList,weight=weightLabel)
    subSparseMembershipM=sparseMembershipM[:len(attribAVals),len(attribAVals):]
    convertedDf=pd.DataFrame(subSparseMembershipM.todense(),index=attribAVals,columns=attribBVals)
    return convertedDf
def getSrrTopTermHits(srr,sraToTermScoringDF,ntopHit=10):
    termhitSeries=sraToTermScoringDF.loc[srr]
    termhitSeries.sort(ascending=False)
    topHitNames=map(  nciIdToStrings,termhitSeries.iloc[:ntopHit].index.values)
    tmpDf=pd.DataFrame([ termhitSeries.iloc[:ntopHit].values.tolist(),topHitNames]).T
    tmpDf.index=termhitSeries.iloc[:ntopHit].index
    tmpDf.columns=["1",'2']
    return tmpDf
    #return pd.DataFrame( [ termhitSeries.iloc[:ntopHit].values.tolist(),topHitNames],index=termhitSeries.iloc[:ntopHit].index.values,columns=["1",'2'])

def DF_MM(DF1, DF2):
    DF2_match_dim=DF2
    M=np.matrix(DF1.as_matrix() )* np.matrix( DF2_match_dim.as_matrix().T )
    return pd.DataFrame( M ,DF1.index, DF2_match_dim.index)
"""
this fuction match the dimension of the first matrix

force DF2 into the shape of DF2, fill 0 if dimension don't exist
"""
def DF_MATCH_DIM_MM(DF1,DF2):
    tmpDF2= DF2.loc[:,DF1.columns].fillna(0.0)
    return DF_MM( DF1,tmpDF2)

"""
L1
this functional should normalize the first matrix
"""
def normalizeDF(DF):

    return pd.DataFrame(np.divide(np.matrix(DF.as_matrix()),
                     np.matrix(DF.as_matrix().sum(axis=1)).T )
                        ,index=DF.index,columns=DF.columns).fillna(0.0)
def save_sparse_csr(filename,array):
    np.savez(filename,data = array.data ,indices=array.indices,
             indptr =array.indptr, shape=array.shape )

def load_sparse_csr(filename):
    loader = np.load(filename)
    return csr_matrix((  loader['data'], loader['indices'], loader['indptr']),
                         shape = loader['shape'])
def saveSparseM( fileDir,csrM,index,columns):
    with open(fileDir+'.index','w') as f:
        f.write('\n'.join(index))
    with open(fileDir+'.columns','w') as f:
        f.write('\n'.join(columns))
    save_sparse_csr(fileDir+'.npz',csrM)
def loadSparseM( fileDir):
    with open(fileDir+'.index','r') as f:
        index=f.read().split('\n')
    with open(fileDir+'.columns','r') as f:
        columns=f.read().split('\n')
    csrM=load_sparse_csr(fileDir+'.npz')  
    return csrM,index,columns
