import sys
import pandas as pd
import param
import os 
i=int(sys.argv[1])-1
#i=0
CWD='/cellar/users/btsui/Project/METAMAP/notebook/RapMapTest/Pipelines/snp/'
os.chdir(CWD)

unprocessed_meta_df=pd.read_csv(param.unprocessed_meta_dir)
myS=unprocessed_meta_df.iloc[i]
print ('LibraryLayout: ',myS['LibraryLayout'])
if myS['LibraryLayout']=='SINGLE':
        cmd='python single_snp.py '+myS.Run+' '+myS['new_ScientificName']
        os.system(cmd)
if myS['LibraryLayout']=='PAIRED':
        cmd='python paired_snp.py '+myS.Run+' '+myS['new_ScientificName']
        os.system(cmd)