
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
from sharedVariable import *
from scipy import sparse
from sklearn.cluster import KMeans
import sys
import os
#number of terms 8547
"""
input: index
output: NCI_id[index] 's kmean centroids (DF) and membership assignment (DF)
"""
CWD='/cellar/users/btsui/Project/CancerSpliceIsoform/GEO/DATA_PROCESSING/IpythonNotebook/'

os.chdir(CWD)


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

sraToNCIDF=loadDf(BioSample.bioSampleAnnotationSrrDir) 
#sraToNCIDF=loadDf(SRAToNCIDPropagatedFPickleFname)
transcriptToSRA=loadDf(transcriptBySraDir)
transcriptMask=map(lambda s:transcriptPrefix in s,transcriptToSRA.index)


# #run Kmean (I)

# In[ ]:

#i=19
i=int (sys.argv[1])-1
from sklearn.metrics import silhouette_score
clusterScoreDict={}
tmpS=sraToNCIDF.iloc[:,i]
#tmpS=sraToNCIDF.loc[:,'CL_0000741']
OntoID=tmpS.name
targetSRA=tmpS[np.logical_and(tmpS>0 ,tmpS.index.isin(transcriptToSRA.columns))].index
tissueSubDF=transcriptToSRA.loc[transcriptMask,targetSRA].T
tissueSubMatrix= tissueSubDF.as_matrix().astype(np.float64)

print 'n sample: ',tissueSubMatrix.shape[0]
#output the first score that stops improving, i.e. increasing one will make things worse
bestResult=None
bestCluster_centers_=None
bestSilhouette_score=-1
#tissueSubMatrix=tissueSubMatrix[:,:50]
silhouetteScoreDict={}
for nCluster in range(2,maxNClusters):
    
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
basePath=kmeanPath+OntoID
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

with open(basePath+str(i)+outputPostfix,'w') as f:
    f.write()

#
#np.save(basePath+kmeanAssignmentExtd,bestResult)
#np.save(basePath+kmeanCentroidExtd,bestCluster_centers_)

