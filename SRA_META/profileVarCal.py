import sys
import numpy as np
sys.path.append('/cellar/users/btsui/Project/METAMAP/code/metamap')
import sharedVariable as shv
import pandas as pd
import os
inDir='/oasis/btsui/Data/SRA/MATRIX/DATA/hgGRC38/'
inDfName='allSRAspliceVariantMaxMatrix'


inDF=inDir+inDfName
sraByTrscrptDF=shv.loadDf(inDF).astype(np.float64)
profileLocation='/cellar/users/btsui/Data/nrnb01_nobackup/METAMAP/'
profileMembershipExtd='.kmeanMembership.merged.pyc'
profileMembershipSDir=profileLocation+inDfName+profileMembershipExtd

outDfName=profileLocation+inDfName+'.var.merged.pyc'

profileMembershipS=pd.read_pickle(profileMembershipSDir)
from collections import defaultdict
profileToSrrDict=defaultdict(set)
for srr,profile in profileMembershipS.iteritems():
    profileToSrrDict[profile].add(srr)
    
myDict={}
for profile,Srrs in profileToSrrDict.iteritems():
    subDf=sraByTrscrptDF.loc[:,Srrs]
    myDict[profile]=pd.Series(subDf.as_matrix().var(axis=1),index=subDf.index)
trscrptByProfileVarDf=pd.DataFrame(myDict)
trscrptByProfileVarDf.to_pickle(outDfName)
