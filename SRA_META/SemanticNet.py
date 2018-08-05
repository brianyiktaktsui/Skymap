__author__ = 'btsui'
import subprocess as sp
import os
import networkx as nx
class SemanticNet:
    SULink='http://semanticnetwork.nlm.nih.gov/Download/UnitFile/SU'
    SRSTRLink='http://semanticnetwork.nlm.nih.gov/Download/RelationalFiles/SRSTR'
    SUFname='SU'
    SRSTRFname='SRSTR'
    hierachy=None

    def _parseForAbbrNameTuple(self,record):
        lines=record.split('\n')

        semanticNameLines=filter( lambda l: any ( map( lambda term:term in l, {'STY:','RL:'} )),lines)
        abbrLines=filter( lambda l:'ABR:'in l,lines)
        if len(semanticNameLines)<1 or len(abbrLines)<1:
            return None
        else:
            semanticNameLine=semanticNameLines[0]
            myName=semanticNameLine.split(': ')[1]
            abbr=abbrLines[0].split(': ')[1]
            return (myName,abbr)

    def getAbbreviationDict(self):
        if not os.path.isfile(self.SUFname):
            sp.call(['wget',self.SULink])
        with open(self.SUFname) as f:
            content=f.read()
        records=filter(lambda r:r!='',content.split('\n\n'))
        parsedRecords=map(self._parseForAbbrNameTuple, records )
        return {r[0]:r[1] for r in  parsedRecords if r != None}

    def _contructHierachy(self):
        if not os.path.isfile(self.SRSTRFname):
            sp.call(['wget',self.SRSTRLink])
        self.hierachy=nx.DiGraph()
        with open(self.SRSTRFname) as f:

            for l in f:
                strs=l.split('|')
                u,e,v=strs[0],strs[1],strs[2]
                if e in {'isa','occurs_in','part_of'}:
                    self.hierachy.add_edge(u,v)
                    self.hierachy[u][v]['eng']=e

    def getChildren(self,Node,abbr=False):
        childrenNodes=nx.bfs_tree(self.hierachy,Node,reverse=True ).nodes()
        abbrD=self.getAbbreviationDict()
        return [abbrD[n] for n in childrenNodes]if abbr else childrenNodes
    def __init__(self):
        self._contructHierachy()
if __name__=='__main__':
    s=SemanticNet()
    #shg.createNetwork(s.getChildren('Anatomical Structure'))
    childrenAbbrvs=s.getChildren('Anatomical Structure',True)+\
    s.getChildren('Natural Phenomenon or Process',True)
    print childrenAbbrvs