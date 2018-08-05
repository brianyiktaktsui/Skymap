__author__ = 'btsui'
import subprocess as sp
import os
import sys
import time
import metamapParam
from SemanticNet import  SemanticNet
class Metamap:
    #check
    metamapBinDir='/cellar/users/btsui/Program/public_mm/bin//'
    params=['-I']
    outputPostfix='.out'
    scriptName='metamapWrapper.sh'
    def __init__(self):
        print 'metamap'

    def process(self,fname):
        #myParams=[]
        SemNet=SemanticNet()
        childrenAbbr=reduce(lambda a,s: a.union(set(SemNet.getChildren(s,abbr=True))), metamapParam.MetaMapSemantics,set() )

        myParams=self.params+metamapParam.MetaMapExtraParams
        print 'processing : ',fname
        #default params

        if True or ( not ( os.path.isfile( fname+self.outputPostfix) and os.stat(fname+self.outputPostfix).st_size>5000) ):
            sp.call([self.metamapBinDir+"skrmedpostctl","start"])
            sp.call([self.metamapBinDir+"wsdserverctl","start"])
            #sp.call([self.metamapBinDir+"metamap"]+myParams+['-J',",".join(childrenAbbr)]+[ fname])
            sp.call([self.metamapBinDir+"metamap"]+myParams+[ fname])
        else:
            print 'memoised'

if __name__=='__main__':

    M=Metamap()
    fname=sys.argv[1]
    M.process(fname)
