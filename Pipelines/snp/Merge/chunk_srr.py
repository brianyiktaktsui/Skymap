#input: list of pickles
tmp_dir='/nrnb/users/btsui/Data/all_seq/tmp_chunks/'
#output: list of pickles
outDir='/cellar/users/btsui/Data/merged/snp/hg38/mergedBySRR/'
import os
import sys
import gc
##allow one version that chunk by 
chunkSize=10**5
maxSrrId=6343458+chunkSize#6343458
myChunks=list(range(0,maxSrrId,chunkSize))
from multiprocessing import Pool



if __name__ == "__main__":
    ith_chunk=int(sys.argv[1])
    #ith_chunk=1
    myL=os.listdir(tmp_dir)
    import numpy as np
    import pandas as pd
    from tqdm import tqdm
    len(myChunks)
    chunk_i=myChunks[ith_chunk]
    
    def extractBlockDf(tmpDfName):
        if tmpDfName.endswith('.pickle.gz'):
            tmpDf=pd.read_pickle(tmp_dir+tmpDfName)
            #chunk index array
            chunk_a=(tmpDf.index.get_level_values('Run_digits')/chunkSize).astype(int)*chunkSize
            m=(chunk_a==chunk_i)
            myChunkDf=tmpDf[m].copy()
            return myChunkDf
        else:
            return None
    
    with Pool(16) as p:
        myChunkDfL=list(tqdm(p.imap(extractBlockDf,myL),total=len(myL)))
        gc.collect()
    myMergedChunkDf=pd.concat(myChunkDfL,axis=0,copy=False)
    myMergedChunkDf.to_pickle("{}/{}.pickle.gz".format(outDir,chunk_i),compression='gzip')
