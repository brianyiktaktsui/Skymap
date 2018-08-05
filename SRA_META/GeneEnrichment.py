__author__ = 'btsui'
import pandas as pd
import numpy as np
import geneEnrichmentParam as param
param=reload(param)
#geneEnrichmentParam=reload(geneEnrichmentParam)
from scipy.sparse import coo_matrix,csr_matrix
class GeneEnrichment:
    def generateSparseDF(self,geneToI):
        #load enrichment dataframe
        self.geneToI= geneToI
        rawDf=pd.DataFrame.from_csv(param.enrichmentFileDir,sep='\t').dropna()
        olgasCode={'IDA','EXP','IPI','IGI','IEP'}
        oldCode={'IDA','EXP','IPI','IGI'}
        codes=olgasCode
        df=rawDf[(rawDf.index.isin(geneToI.index))&(rawDf['GO Term Evidence Code'].isin(codes))]
        genes=df.index.unique()
        gos=df['GO Term Name'].unique()
        self.goToJ=pd.Series(range(len(gos)),index=gos)
        self.JToG=pd.Series(gos,index=range(len(gos)))
        #zip the transcr
        J=self.goToJ[df['GO Term Name'].values].values
        I=self.geneToI[df.index].values
        binArray=np.zeros(shape=(len(I)))
        binArray.fill(1)
        coo_M=coo_matrix( (binArray,(I,J)),shape=(geneToI.max()+1,len(gos)))#.reshape((len(I),len(J)))
        self.csr_M=coo_M.tocsr()
    def __init__(self,geneToI=None):
        if geneToI==None:
            geneToI=pd.load(param.geneToIDir)
        self.generateSparseDF(geneToI)