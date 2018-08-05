__author__ = 'btsui'
import sharedFunctionParsing as shv
class querySystem:
    #def __init__(self,):
    def loadMatrices(self,pathToSynonymQueryMatrices, nSynonym):
        return [shv.loadDf(pathToSynonymQueryMatrices+'.'+str(i)) for i in range(nSynonym)]
    def getUnionDimension(self,queryMatrices):
        """

        :param queryMatrices:
        :return: the features of rows and columns, union of all matrices
        """
        allIndex=reduce(lambda a,DF:a.union( set(DF.index) ), queryMatrices,set())
        allColumn=reduce(lambda a,DF:a.union( set(DF.columns) ), queryMatrices,set())
        return allIndex,allColumn
    def queryWithSynonym(self,terms,pathToSynonymQueryMatrices,pathToSampleMatrix,nSynonym,threshold=500.0):
        """

        :param pathToSynonymQueryMatrices:
        :param pathToSampleMatrix:
        :return: a query by hit, score matrix.
        """
        import numpy as np
        """
        psuedo code:
            load in all synonym matrices
            load in biosample matrix

            for each synon matric:
                query against sample matrix and update the best score
        """

        inputMatrices= self.loadMatrices(pathToSynonymQueryMatrices,nSynonym)

        queryMatrices=map(lambda matrix:matrix.loc[terms] ,inputMatrices )
        allIndex,allColumn= self.getUnionDimension(queryMatrices)
        tmpBioSampleDF=shv.loadDf(pathToSampleMatrix).abs()
        bioSampleDF=(tmpBioSampleDF>=threshold).astype(np.float64)
        returnDF=shv.createEmptyDf(allIndex,bioSampleDF.index)

        for rawSynonDF in queryMatrices:
            binarizedDense=(rawSynonDF>=threshold).astype(np.float64)
            s=binarizedDense.sum(axis=0)
            synonDF=binarizedDense[ s[~(s==s.max())].index]

            normedSynonymDF=shv.normalizeDF(synonDF)
            subSetBioSampleDF=bioSampleDF.loc[:,normedSynonymDF.columns].fillna(0)

            myM=np.matrix(normedSynonymDF)*np.matrix(subSetBioSampleDF).T
            returnDF.loc[normedSynonymDF.index,:]=\
                np.maximum(returnDF.loc[normedSynonymDF.index,:],myM)
        return returnDF
    def queryWithSynonymMultimappingReduction(self,terms,pathToSynonymQueryMatrices,pathToSampleMatrix,nSynonym,threshold=500.0):
        """

        :param pathToSynonymQueryMatrices:
        :param pathToSampleMatrix:
        :return: a query by hit, score matrix.
        """
        import numpy as np
        import pandas as pd
        """
        psuedo code:
            load in all synonym matrices
            load in biosample matrix

            for each synon matric:
                query against sample matrix and update the best score
        """

        inputMatrices= self.loadMatrices(pathToSynonymQueryMatrices,nSynonym)

        queryMatrices=map(lambda matrix:matrix.loc[terms] ,inputMatrices )
        allIndex,allColumn= self.getUnionDimension(queryMatrices)
        tmpBioSampleDF=shv.loadDf(pathToSampleMatrix).abs()
        bioSampleDF=(tmpBioSampleDF>=threshold).astype(np.float64)
        returnDF=shv.createEmptyDf(allIndex,bioSampleDF.index)
        myDict={}
        for i,rawSynonDF in enumerate(queryMatrices):
            binarizedDense=(rawSynonDF>=threshold).astype(np.float64)
            s=binarizedDense.sum(axis=0)
            synonDF=binarizedDense[ s[~(s==s.max())].index]

            normedSynonymDF=shv.normalizeDF(synonDF)
            subSetBioSampleDF=bioSampleDF.loc[:,normedSynonymDF.columns].fillna(0)

            myM=np.matrix(normedSynonymDF)*np.matrix(subSetBioSampleDF).T
            returnDF.loc[normedSynonymDF.index,:]=\
                np.maximum(returnDF.loc[normedSynonymDF.index,:],myM)
            myDict[i]=(returnDF.T>=0.8).astype(np.float64).sum(axis=1)
        return pd.DataFrame(myDict)