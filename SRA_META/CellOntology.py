__author__ = 'btsui'
import networkx as nx
import cellOntologyParam as param
param=reload(param)
import networkx as nx
from xml.etree.ElementTree import iterparse
import pandas as pd
import numpy as np

import os
import sharedVariable as shv
class CellOntology:
    cellOnto=None
    cleanedIdS=None
    def _readOnto(self):
        tmpGraph=nx.read_gpickle(param.cellDir)
        #rename node to have just ID, but not URL
        self.cellOnto=nx.relabel_nodes(tmpGraph, {n:n.split('/')[-1] for n in tmpGraph.nodes_iter() })
        s=pd.read_pickle(param.cleanIdDir)
        self.cleanedIdS=pd.Series(s.values,map(lambda term:term.split('/')[-1], s.index) ).drop_duplicates()
    """
    input: terms
    output: children terms
    """
    def childrenTermsOf(self,node,eng=False):
        children=nx.bfs_tree(self.cellOnto,node,reverse=True).nodes()
        return [self.cleanedIdS[c] for c in children]  if eng else children


    def convertIdsToEng(self,ids):
        return self.cleanedIdS[ids]

    def _init_UMLSDF(self,fname):
        import sharedFunctionParsing as shp
        shp=reload(shp)
        shp.convertFileToUMLSDF(fname)
    def populateGraphWithDF(self,CellOntoByDtypeDF):
        for cellOntoTerm , dtypeS in CellOntoByDtypeDF.iterrows():
            if cellOntoTerm in self.cellOnto.node:
                for dtype,value in dtypeS.iteritems():
                    self.cellOnto.node[cellOntoTerm][dtype]=value

    def getDenseGraph(self,inputG,threshold=0):
        for n in inputG:
            inputG.node[n]['step_wise_weight']=int(inputG.node[n]['sum'] > threshold)
        return inputG

    def populateOntoCytoScape(self,node,reverse=False,dense=False,threshold=0):
        import sharedFunctionGraph as shg
        shg=reload(shg)
        myTerms=self.childrenTermsOf(node)
        subGraph=nx.subgraph(self.cellOnto,myTerms)
        for n in subGraph.nodes_iter():
            subGraph.node[n]['eng']=self.cleanedIdS[n]
        print nx.is_directed_acyclic_graph(subGraph)
        displayingGraph= self.getDenseGraph(subGraph,threshold) if dense else subGraph

        shg.createNetwork(displayingGraph.reverse() if reverse else displayingGraph,layout='force-directed')

    def generateGrouping(self,node):
        """
        :param nodes:

        group weight=0 , child
        group weight =1, group leader
        :return:
        """
        revCellOnto=self.cellOnto.reverse()
        topLevelChildren=set(revCellOnto.out_edges ( node))
        for _,child in topLevelChildren:
            self.cellOnto.node[child]['grouping']=self.cleanedIdS[child]
            self.cellOnto.node[child]['group_weight']=1
            for n in nx.bfs_tree(revCellOnto,child).nodes_iter():
                if n not in topLevelChildren:
                    self.cellOnto.node[n]['grouping']=self.cleanedIdS[child]
                    self.cellOnto.node[n]['group_weight']=0
        for u,v in self.cellOnto.edges_iter():
            if all( map(lambda n :'grouping' in self.cellOnto.node[n] ,[u,v])) and \
                self.cellOnto.node[u]['grouping']==self.cellOnto.node[u]['grouping']:
                    self.cellOnto[u][v]['edge_group']=self.cellOnto.node[u]['grouping']
            else:
                    self.cellOnto[u][v]['edge_group']='cross'

    def getSubUMLSDF(self,terms,threshold=500,filterOverlyPrevalent=True):
        """
        input : terms: list of terms where their children should be incoperated
        output: sub UMLS matrix

        param: filterOverlyPrevalent: filter out the most prevalent terms
        NOTE: this one has no synonyms optimzation
        """
        dfFname=param.CellOntologyToUMLSDFDir
        if not os.path.isfile(dfFname+'.npy'):
            self._init_UMLSDF(dfFname)
        nodes= reduce(lambda a,term: a.union(set(self.childrenTermsOf(term)))  , terms,set())
        cellOntoUMLSDF=shv.loadDf(dfFname).abs()
        myUMLSSubDF=cellOntoUMLSDF.loc[nodes]
        myUMLSSubDF=myUMLSSubDF.fillna(0)
        denseSubDF=myUMLSSubDF.loc[:,myUMLSSubDF.any(axis=0)]
        binarizedDense=(denseSubDF>threshold).astype(np.float64)

        if filterOverlyPrevalent:
            s=binarizedDense.sum(axis=0)
            binarizedDense=binarizedDense[ s[~(s==s.max())].index]

        return binarizedDense
    def binarizeUMLSDF(self,cellOntoUMLSDF,term,threshold=500,filterOverlyPrevalent=True):

        nodes=self.childrenTermsOf(term)
        myUMLSSubDF=cellOntoUMLSDF.loc[nodes]
        myUMLSSubDF=myUMLSSubDF.fillna(0)
        denseSubDF=myUMLSSubDF.loc[:,myUMLSSubDF.any(axis=0)]
        binarizedDense=(denseSubDF>threshold).astype(np.float64)

        if filterOverlyPrevalent:
            s=binarizedDense.sum(axis=0)
            binarizedDense=binarizedDense[ s[~(s==s.max())].index]
        return binarizedDense
    def queryMatrix(self,matrix):
        """

        :param matrix:
        :return:
        """
        return
    def __init__(self):
        self._readOnto()