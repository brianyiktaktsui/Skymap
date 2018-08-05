
# coding: utf-8

# #objective
# 
# find a way to identify the best k
# 
# 
# current heuristics: 
# find the first k that fails to improve, starting from 1

# In[ ]:

import sys
sys.path.append('/cellar/users/btsui/Project/METAMAP/code/metamap')
from BioSample import BioSample


# In[ ]:

__author__ = 'btsui'

from scipy import sparse
from sklearn.cluster import KMeans
from sharedVariable import *
import sys
import os
#number of terms 8547
"""
input: index
output: NCI_id[index] 's kmean centroids (DF) and membership assignment (DF)
"""
CWD='/cellar/users/btsui/Project/CancerSpliceIsoform/GEO/DATA_PROCESSING/IpythonNotebook/'




#
kmeanSilhouetteExtd='.silh.pyc'
kmeanAssignmentExtd=".membership.pyc"
kmeanCentroidExtd=".centroid.pyc"
outputPostfix='.success'
#outputMatrixName
outputMatrixName=transcriptBySraDir+".GTEXSRAByTerm_Score"
nonModuleOutputMatrixName=transcriptBySraDir+".GTEXSRAByAllSra_Score"
nonModuleOutputRankResultMatrixName=transcriptBySraDir+".GTEXSRAByRank_Sra"


# #try running one run of kmean

# In[ ]:

#i=int (sys.argv[1])-1

def func(Dir):
    from sklearn.metrics import silhouette_score

    os.chdir(CWD)
    clusterScoreDict={}
    #tmpS=sraToNCIDF.loc[:,'CL_0000741']
    tissueSubDF=loadDf(Dir).T 
    print tissueSubDF.shape
    tissueSubMatrix= tissueSubDF.as_matrix().astype(np.float64)
    
    print 'n sample: ',tissueSubMatrix.shape[0]
    #output the first score that stops improving, i.e. increasing one will make things worse
    bestResult=None
    bestCluster_centers_=None
    silhouetteScoreDict={}
    bestSilhouette_score=-100000
    for nCluster in range(maxNClusters,maxNClusters+1):

        kmean=KMeans(n_clusters=nCluster,n_jobs=1,precompute_distances=True)
        kmean.fit( tissueSubMatrix)
        result=kmean.transform(tissueSubMatrix)
        mySilhouette_score=silhouette_score(tissueSubMatrix,kmean.labels_)
        silhouetteScoreDict[nCluster]=mySilhouette_score
        print nCluster,mySilhouette_score
        if mySilhouette_score<bestSilhouette_score:
            break
        else:
            bestCluster_centers_=kmean.cluster_centers_
            bestResult=result
            bestSilhouette_score=mySilhouette_score
            bestLabels=kmean.labels_
    #exporting data
    SRRIds=tissueSubDF.index
    basePath=Dir
    #
    silhouetteVect=pd.Series(silhouetteScoreDict)
    kmeanLabelVect=pd.Series(bestLabels,index=SRRIds)
    kmeanDissimilarityDF=pd.DataFrame(bestResult,index=SRRIds)
    kmeanCentroidDF=pd.DataFrame(bestCluster_centers_)

    kmeanLabelExtd='.label.pyc'
    silhouetteVect.to_pickle(basePath+kmeanSilhouetteExtd)
    kmeanLabelVect.to_pickle(basePath+kmeanLabelExtd)

    kmeanDissimilarityDF.to_pickle(basePath+kmeanAssignmentExtd)
    kmeanCentroidDF.to_pickle(basePath+kmeanCentroidExtd)

    with open(basePath+outputPostfix,'w') as f:
        f.write('   ')
if __name__=='__main__':
    Dir=sys.argv[1]
    func(Dir)
#
#np.save(basePath+kmeanAssignmentExtd,bestResult)
#np.save(basePath+kmeanCentroidExtd,bestCluster_centers_)

