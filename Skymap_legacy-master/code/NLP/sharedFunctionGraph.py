__author__ = 'btsui'
import networkx as nx
#filter nodes where there is no children that have any number
#graph
landscapeGraphDir='SraDataStatGraph.pyc'
import requests
import json
import pandas as pd
import numpy as np
import math
import os
from py2cytoscape import util
NciPickleBaseDir="/cellar/users/btsui/Project/CancerSpliceIsoform/GEO/DATA_PROCESSING/IpythonNotebook/"

NCIRelToEngDir=NciPickleBaseDir+'NCIRelToEng.pyc'
metaDFDir=NciPickleBaseDir+'NCIT.csv'
NCIRelToEng=pd.read_pickle(NCIRelToEngDir)
metaDF=pd.DataFrame.from_csv(metaDFDir)

NCIIdToEng=metaDF['Preferred Label']
NCIIdToEng.index=map(lambda s:s.split('#')[1], NCIIdToEng.index)

def densifyGraph(inG):
    #mark
    tmpG=inG.copy()

    #topologically propagate the node count
    edgeOrder=tmpG.in_edges(nx.topological_sort(tmpG) )
    for u,v in edgeOrder:
        tmpG.node[v]['count']+=tmpG.node[u]['count']
    nonEmptNodes=[n for n,d in tmpG.nodes_iter(data=True) if d['count']>0 ]
    g=inG.subgraph(nonEmptNodes)
    return g

"""
find node that get touched at all
"""
#need to generate a matrix
"""
myDF columns are features:

"""

def newDF(index,column):
    return pd.DataFrame(np.zeros( (len(index),len(column)) ,dtype=np.float64),index=index ,columns=column )
def graphPropagateDF(myG, myDF):
    outDF=newDF(myDF.index ,myG.nodes())
    outDF[myDF.columns]=myDF[myDF.columns]
    edgeOrder=myG.in_edges(nx.topological_sort(myG) )
    i=0
    for u,v in edgeOrder:
        i+=1
        outDF[v]+=outDF[u]
    binarizedDF=(outDF>=1.0).astype(np.float64)
    return binarizedDF


# Basic Setup
PORT_NUMBER = 1234
BASE = 'http://localhost:' + str(PORT_NUMBER) + '/v1/'
print BASE
# Header for posting data to the server as JSON
HEADERS = {'Content-Type': 'application/json'}

def createNetwork(network,layout='hierarchical'):
    cytoscapeNetwork=util.from_networkx(network)
    res1=requests.post(BASE + 'networks', data=json.dumps(cytoscapeNetwork), headers=HEADERS)
    res1_dict = json.loads(res1.content)
    print res1.content
    #print res1_dict['networkSUID']
    new_suid = res1_dict['networkSUID']
    requests.get(BASE + 'apply/layouts/'+layout+'/' + str(new_suid))
    requests.get(BASE + 'apply/styles/SRALandscape/' + str(new_suid))

def annnotateGraph(denseG,ConversionS=NCIIdToEng):
    newG=denseG.copy()
    for n in newG.nodes_iter():
        
        newG.node[n]['eng']=ConversionS[n] if n in ConversionS else str(n)
    for u,v ,d in newG.edges_iter(data=True):
        if 'rel' in d:
            eng= 'is_a' if d['rel']=='is_a' else ConversionS[d['rel']] if n in ConversionS else d['rel']
            newG[u][v]['eng']=eng
    return newG
"""

def sumTransformGraph(denseG,dtypes):
    newG=denseG.copy()
    for n, d in newG.nodes_iter(data=True):
        mySum=0
        for k,v in d.iteritems():
            if k in dtypes:
                mySum+=v

        newG.node[n]['sum']=mySum
        newG.node[n]['log_sum']=math.log(mySum) if mySum>0 else 0
    return newG
"""
def sumTransformGraph(denseG,dtypes,prefix=''):
    newG=denseG.copy()
    for n, d in newG.nodes_iter(data=True):
        mySum=0
        for k,v in d.iteritems():
            if k in dtypes:
                mySum+=v

        newG.node[n][prefix+'sum']=mySum
        newG.node[n][prefix+'log_sum']=math.log(mySum) if mySum>0 else 0
    return newG