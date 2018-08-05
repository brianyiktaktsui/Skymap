__author__ = 'btsui'
from clusterBaseClass import clusterBaseClass
import pandas as pd 
class Merger:
    def mergeDFs(self,fnames,outDFName):
        """
        input: 
        """
        listOfSeries=[pd.read_pickle(fname+'.npy') for fname in fnames ]
        mergedSeries=pd.concat(listOfSeries)
        mergedSeries.to_pickle(outDFName+'.pyc')
        """
        dfDict={fname:shv.loadDf(fname) for fname in fnames}
        index= reduce (lambda a,S:a.union(set(S.index.tolist())) , dfDict.values(), set())
        columns= reduce (lambda a,S:a.union(set(S.columns)) , dfDict.values(), set())
        DF=shv.createEmptyDf(index,columns )
        for df in dfDict.itervalues():
            DF.loc[df.index,df.columns]= df.loc[df.index,df.columns]
        shv.exportDf(outDFName,DF.abs())
        """