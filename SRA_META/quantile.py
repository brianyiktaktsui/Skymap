__author__ = 'btsui'
myPostfix='.quant'
outputPostfix=myPostfix+'.npy'

import sys
sys.path.append('/cellar/users/btsui/Project/METAMAP/code/metamap')
from BioSample import BioSample
__author__ = 'btsui'
import sys
import os
import sharedVariable as sh

def func(Dir):

    #[IMPORTANT]TAKE THIS LINE OUT WHEN DONE
    tissueSubDF=sh.loadDf(Dir)
    outDF=tissueSubDF.rank(axis=0)
    sh.exportDf(Dir+myPostfix,outDF)
if __name__=='__main__':
    Dir=sys.argv[1]
    func(Dir)