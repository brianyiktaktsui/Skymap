__author__ = 'btsui'
import networkx as nx
import NCITerminologyParam as param
#param=reload(param)
import networkx as nx
from xml.etree.ElementTree import iterparse
import pandas as pd
import numpy as np

import os
import sharedVariable as shv

class NCITerminology:
    cellOntoSubset=None
    cellOnto=None
    cleanedIdS=None
    idToUMLS=None
    relToEng=None
    def _readOnto(self):
        self.allEdgeDf=pd.DataFrame.from_csv(param.edgeListDir)
        tmpGraph=nx.from_pandas_edgelist(df=self.allEdgeDf,source='src',target='dest',edge_attr=['rel'],create_using=nx.DiGraph())
        #rename node to have just ID, but not URL
        self.cellOnto=nx.relabel_nodes(tmpGraph, {n:n.split('/')[-1] for n in tmpGraph.nodes() })
        self.cellOntoSubset=self.cellOnto
        s=pd.read_pickle(param.cleanIdDir)
        #read id to eng
        self.cleanedIdS=pd.Series(s.values,map(lambda term:term.split('/')[-1], s.index) ).drop_duplicates()
        #read id to UMLS
        self.idToUMLS=pd.read_pickle(param.idToUMLSDir)
        denseS=self.idToUMLS.dropna()
        self.UMLSToID=pd.Series(denseS.index, denseS.values)
        self.relToEng=pd.read_pickle(param.relToEngDir)
        self.cleanedIdS.loc['root_node']='root'
    """
    input: terms
    output: children terms
    """
    def setCellOntoEdgeSubset(self,rels):
        tmpDf=self.allEdgeDf[self.allEdgeDf.rel.isin(rels)]
        self.cellOntoSubset=nx.nx.from_pandas_edgelist(df=tmpDf,source='src',target='dest',edge_attr=['rel'],create_using=nx.DiGraph())
        
        """
        self.cellOntoSubset=nx.DiGraph()
        for u,v,d in self.cellOnto.edges_iter(data=True):
            if d['rel'] in rels:
                self.cellOntoSubset.add_edge(u,v,attr_dict=d)
        print 'is graph weakley connected?: ',nx.is_weakly_connected(self.cellOntoSubset)
        """
    def childrenTermsOf(self,node,eng=False):
        children=nx.bfs_tree(self.cellOntoSubset,node,reverse=True).nodes()
        return [self.cleanedIdS[c] for c in children]  if eng else children
    def getEdgeTypes(self):
        return {d['rel'] for u,v, d in self.cellOntoSubset.edges_iter(data=True) if 'rel' in d}
    def convertIdsToEng(self,ids):
        return self.cleanedIdS[ids]

    def _init_UMLSDF(self,fname):
        import sharedFunctionParsing as shp
        shp=reload(shp)
        shp.convertFileToUMLSDF(fname)
    def populateGraphWithDF(self,CellOntoByDtypeDF):
        for cellOntoTerm , dtypeS in CellOntoByDtypeDF.iterrows():
            if cellOntoTerm in self.cellOntoSubset.node:
                for dtype,value in dtypeS.iteritems():
                    self.cellOntoSubset.node[cellOntoTerm][dtype]=value

    def getDenseGraph(self,inputG,threshold=0):
        for n in inputG:
            inputG.node[n]['step_wise_weight']=int(inputG.node[n]['sum'] > threshold)
        return inputG

    def populateOntoCytoScape(self,node,reverse=False,dense=False,threshold=0):
        import sharedFunctionGraph as shg
        shg=reload(shg)
        myTerms=self.childrenTermsOf(node)
        subGraph=nx.subgraph(self.cellOntoSubset,myTerms)
        for n in subGraph.nodes_iter():
            subGraph.node[n]['eng']=self.cleanedIdS[n]
        #print nx.is_directed_acyclic_graph(subGraph)
        displayingGraph= self.getDenseGraph(subGraph,threshold) if dense else subGraph
        shg.createNetwork(displayingGraph.reverse() if reverse else displayingGraph,layout='force-directed')

    def generateGrouping(self,node):
        """
        :param nodes:

        group weight=0 , child
        group weight =1, group leader
        :return:
        """
        revCellOnto=self.cellOntoSubset.reverse()
        topLevelChildren=set(revCellOnto.out_edges ( node))
        for _,child in topLevelChildren:
            self.cellOntoSubset.node[child]['grouping']=self.cleanedIdS[child]
            self.cellOntoSubset.node[child]['group_weight']=1
            for n in nx.bfs_tree(revCellOnto,child).nodes_iter():
                if n not in topLevelChildren:
                    self.cellOntoSubset.node[n]['grouping']=self.cleanedIdS[child]
                    self.cellOntoSubset.node[n]['group_weight']=0
        for u,v in self.cellOntoSubset.edges_iter():
            if all( map(lambda n :'grouping' in self.cellOntoSubset.node[n] ,[u,v])) and \
                self.cellOntoSubset.node[u]['grouping']==self.cellOntoSubset.node[u]['grouping']:
                    self.cellOntoSubset[u][v]['edge_group']=self.cellOntoSubset.node[u]['grouping']
            else:
                    self.cellOntoSubset[u][v]['edge_group']='cross'

    def __init__(self):
        self._readOnto()
