#!/cellar/users/btsui/anaconda2/bin/python
import param as param
import pandas as pd
import numpy as np
import os
CWD='/cellar/users/btsui/Project/METAMAP/notebook/RapMapTest/Pipelines/RNAseq/'
os.chdir(CWD)
allProcessedFnames=pd.Series(os.listdir(param.count_out_dir),dtype=np.str)
processed_runs=allProcessedFnames.str.extract('([DRS]RR\d+)',expand=False).values
print processed_runs
allDF=pd.DataFrame.from_csv(param.full_meta_dir)
#m1=True#
m1=(~allDF.index.isin(processed_runs))

#m2=(allDF['pipe_line'].isin(param.supporting_seqs))
m2=allDF['LibraryStrategy'].isin(param.supporting_library_strategy)
m3=allDF['new_ScientificName'].isin(param.supporting_species)
m4=(allDF.Status=='live')
m5=(allDF.proj_accession_Visibility=='public')
m6=(allDF.Bases>(1*((10**6))))
m7=allDF.LibraryLayout.isin(param.supporting_layouts)
m8=~allDF["Study"].isin(['ERP013950'])
targetMetaDF=allDF[ m1&m2&(m3)&m4&m5&m6&m7&m8].sort_values('Bases')
targetMetaDF.to_csv(param.unprocessed_meta_dir)

command="qsub -t 1-"+str(targetMetaDF.shape[0])+" all_seq.sh"
print command
os.system(command)
#log_out_dir='/cellar/users/btsui/Data/SRA/all_seq/log/'
#count_out_dir='/cellar/users/btsui/Data/SRA/all_seq/chip/'
