__author__ = 'btsui'
import sharedVariable as shv
import numpy as np
import pandas as pd
class Entropy:
    baseDir='/cellar/users/btsui/Data/nrnb01_nobackup/Data/SRA/MATRIX/DATA/'
    geneByTrscrptMName='geneByTranscriptVariantMatrixV2'

    def caculateEntropy(self,expDf,psuedoCount=0):
        """

        :param expDf:
        :return: { expr By Gene Entropy Df, expr By Trscrp Entropy Df} in dictionary format
        """
        expM=np.matrix(expDf.as_matrix())+psuedoCount
        exprByGeneM=(expM.T*self.sparseTrscrpByGeneM)
        exprByTrscrpGeneSumM=exprByGeneM*self.sparseTrscrpByGeneM.T
        exprByTrscrpPM=np.nan_to_num(np.divide (expM.T, exprByTrscrpGeneSumM))
        logProbM=np.nan_to_num(np.log2(exprByTrscrpPM))
        exprByTrscrpEntropyM=-np.multiply(exprByTrscrpPM,logProbM)
        
        exprByGeneEntropyM=np.matrix(exprByTrscrpEntropyM)*self.sparseTrscrpByGeneM
        #exporting phase
        exprs=expDf.columns
        transcripts=expDf.index
        genes=self.orderedGeneByTrscrpMColumns
        exprByGeneEntropyDf=pd.DataFrame(data=exprByGeneEntropyM,index=exprs,columns=genes)
        exprByTrscrpEntropyDf=pd.DataFrame(data=exprByTrscrpEntropyM,index=exprs,columns=transcripts)
        return {'exprByGeneEntropyDf':exprByGeneEntropyDf,'exprByTrscrpEntropyDf':exprByTrscrpEntropyDf}
    def __init__(self):
        self.specie=shv.specie
        self.geneByTrscrptDir=self.baseDir+self.specie+'/'+self.geneByTrscrptMName
        self.sparseTrscrpByGeneM,self.orderedGeneByTrscrpMIndex,self.orderedGeneByTrscrpMColumns = shv.loadSparseM(self.geneByTrscrptDir)

