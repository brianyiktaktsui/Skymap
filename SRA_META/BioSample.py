__author__ = 'btsui'
import BioSampleParam as param
import sharedVariable as shv
import numpy as np
import pandas as pd
import os
"""
def init:
    load xml
"""
class BioSample:
    """
    bioSampleAnnotationDir: contains a comma delimated file, biosampleId appear before the first common
        no headings
    """

    bioSampleAnnotationDir=None
    bioSampleAnnotationSrrDir=None
    bioSampleAnnotation=None
    genomeRawDtypeSrr=None
    fullBioSampleMetaDFDir=''
    ParsedBioSampleAnnotationDir='.processedParsedBio.csv'
    def parseToPandasReadable(self,bioSampleAnnotationDir,ParsedBioSampleAnnotationDir):
        with open(bioSampleAnnotationDir) as f, open(ParsedBioSampleAnnotationDir,'w') as wf:
            wf.write('title\tannotation\n')
            for l in f:
                objs=l.split(',')
                Id=objs[0]
                annot=','.join(objs[1:])
                wf.write(Id+'\t'+annot)

    def query(self,terms,CellByBioSampleDF,topN=3,threshold=0.8):
        """
        :param terms:a set of Cell Ontology terms
        :param CellByBioSampleDF: a cell ontology by biosample DataFrame
        :param topN: top N terms to be returned for each query
        :return:a DF containing hit and annotation
        """
        subCellByBioSampleDF= CellByBioSampleDF.loc[ {term for term in terms if term in CellByBioSampleDF.index}]
        termByRankDict={}
        for term,exprsByScore in subCellByBioSampleDF.iterrows():
            exprsByScoreC=exprsByScore.copy()
            exprsByScoreC.sort(ascending=False)
            exprsByScoreS=exprsByScoreC[exprsByScoreC>threshold]
            topHitDF=self.bioSampleAnnotation.loc[exprsByScoreS.index[:topN]]

            exprs= map(lambda (annot,Id):annot+' ('+Id+')' ,\
                   zip(topHitDF.annotation.tolist(),topHitDF.index.tolist()) )
            rankExprDict={rank: (exprs[rank] if rank < len(exprs) else '')for rank in range(topN)  }
            termByRankDict[term]=rankExprDict

        return pd.DataFrame(termByRankDict)
            #rank 1: CUI: exp
    def upgradeToSrrDF(self,BioByCellSampleDF,cache=True):
        """
        #implicit export: export file to biosampelAnnotation as srr
        #implicit input: self.bioSampleAnnotation
        note: [IMPORTANT] don't cache for first run
        :return: SRR by UMLS DF
        """

        srrConvertedFname=self.bioSampleAnnotationSrrDir

        if not cache or not os.path.isfile(srrConvertedFname+'.npy'):
            if os.path.isfile(shv.cacheName(srrConvertedFname+'.npy')):
                os.remove(shv.cacheName(srrConvertedFname+'.npy'))
            AllBioSampleIds={genome+'_'+dtype: pd.DataFrame.from_csv(Dir+genome+'/metaData.txt').BioSample for genome in shv.genomeBuild for dtype, Dir in shv.baseDirDict.iteritems()}
            srrToBioSampleS=pd.concat(AllBioSampleIds.values())
            inputS=srrToBioSampleS
            returnDF=shv.createEmptyDf( srrToBioSampleS[srrToBioSampleS.isin(BioByCellSampleDF.index)].index.unique(),BioByCellSampleDF.columns )
            for srr,biosample in inputS.iteritems():
                if biosample in BioByCellSampleDF.index:
                    if srr in returnDF.index:
                        returnDF.loc[srr]=BioByCellSampleDF.loc[biosample]
            shv.exportDf(srrConvertedFname,returnDF)
        else:
            returnDF=shv.loadDf(srrConvertedFname)
        return returnDF
    def getDtypeHitVect(self,srrByCellOntoDF,annotate=True):
        """
        log(x+1)
        :param srrByCellOntoDF: srr by Cell Ontology Term, hit score DataFrame
        :return: cell ontology by dtype dfs
        """
        AllBioSampleIds={genome+'_'+dtype: pd.DataFrame.from_csv(Dir+genome+'/metaData.txt').BioSample for genome in shv.genomeBuild for dtype, Dir in shv.baseDirDict.iteritems()}
        returnDict={}
        for dtype, srrIds in  AllBioSampleIds.iteritems():
            subsetSrrIds= srrIds[srrIds.index.isin(srrByCellOntoDF.index)].index
            returnDict[dtype]=srrByCellOntoDF.loc[subsetSrrIds].sum(axis=0)
        returnDF = pd.DataFrame(returnDict)
        if annotate:
            log_sum_S=np.log( returnDF.sum(axis=1)+1)
            sum=returnDF.sum(axis=1)
            returnDF['sum']=sum
            returnDF['log_sum']=log_sum_S
        return returnDF
    def __init__(self,bioSampleAnnotationDir='/cellar/users/btsui/Data/nrnb01_nobackup/METAMAP/input/restrictedAttrib.v3.csv'):
        #load annoataion
        self.bioSampleAnnotationDir=bioSampleAnnotationDir
        self.bioSampleAnnotationSrrDir= bioSampleAnnotationDir+'.srr'

        #self.genomeRawDtypeSrr={genome+'_'+dtype: set(pd.DataFrame.from_csv(Dir+genome+'/metaData.txt').index.values)
        #           for genome in shv.genomeBuild for dtype, Dir in shv.baseDirDict.iteritems()}
        #self.genomeRawDtypeBiosample={genome+'_'+dtype: set(pd.DataFrame.from_csv(Dir+genome+'/metaData.txt').BioSample.values)
        #           for genome in shv.genomeBuild for dtype, Dir in shv.baseDirDict.iteritems()}
        #ProjectID
        #listOfMetaDFs=[pd.DataFrame.from_csv(Dir+genome+'/metaData.txt')
        #           for genome in shv.genomeBuild for dtype, Dir in shv.baseDirDict.iteritems()]
        #self.metaDF=pd.concat(listOfMetaDFs)

        self.parseToPandasReadable(self.bioSampleAnnotationDir,self.ParsedBioSampleAnnotationDir)
        self.bioSampleAnnotation=pd.DataFrame.from_csv(self.ParsedBioSampleAnnotationDir,sep='\t')
        self.metaDF=pd.DataFrame.from_csv(shv.baseMetaDataDir+'allBioSample.doublespace.csv.merged.out.pcbc')
        #self.metaDF=pd.merge(self.metaDF,self.bioSampleAnnotation, left_on='BioSample', right_index=True)

