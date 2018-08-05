
# coding: utf-8

# In[4]:

import pandas as pd
import os
baseOutDir='/data/cellardata/users/btsui/SRA/DUMP/'
inDir='/cellar/users/btsui/Data/nrnb01_nobackup/tmp/METAMAP//splittedInput_SRAMangaer_SRA_META/'
#inDir='/cellar/users/btsui/Data/nrnb01_nobackup/tmp/METAMAP/splittedInput_SRAMangaer_NCBI_SRA_Metadata_Full_20171001/'
subsetIds=set( map(lambda s:s.split('.')[0],os.listdir(inDir)))

len(subsetIds)
srsS=[]
srxS=[]
for Id in subsetIds:
    srsS.append(pd.read_pickle(inDir+Id+'.srs.pickle'))
    srxS.append(pd.read_pickle(inDir+Id+'.srx.pickle'))
srsMergedS=pd.concat(srsS)
srxMergedS=pd.concat(srxS)
srsMergedS.to_pickle(baseOutDir+'allSRS.pickle.gz')
srxMergedS.to_pickle(baseOutDir+'allSRX.pickle.gz')


# In[1]:

#pwd


# In[ ]:



