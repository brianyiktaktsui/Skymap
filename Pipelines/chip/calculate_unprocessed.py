#!/cellar/users/btsui/anaconda2/bin/python
import param as param
import pandas as pd
import os
CWD='/cellar/users/btsui/Project/METAMAP/notebook/RapMapTest/Pipelines/'
os.chdir(CWD)
allProcessedFnames=pd.Series(os.listdir(param.count_out_dir))
processed_runs=allProcessedFnames.str.extract('([DRS]RR\d+)',expand=False).values
print processed_runs
allDF=pd.DataFrame.from_csv(param.full_meta_dir)
#m1=True#
m1=(~allDF.index.isin(processed_runs))
m2=(allDF['pipe_line'].isin(param.supporting_seqs))
m3=allDF.ScientificName.isin(param.supporting_species)
m4=(allDF.Status=='live')
m5=(allDF.proj_accession_Visibility!='controlled_access')
m6=(allDF.Bases>(5*(10**6*30)))
m7=allDF.LibraryLayout.isin(param.supporting_layouts)
targetMetaDF=allDF[ m1&m2&(m3)&m4&m5&m6&m7].sort_values('Bases')
targetMetaDF.to_csv(param.unprocessed_meta_dir)

command="qsub -t 1-"+str(targetMetaDF.shape[0])+" all_seq.sh"
print command
os.system(command)
#log_out_dir='/cellar/users/btsui/Data/SRA/all_seq/log/'
#count_out_dir='/cellar/users/btsui/Data/SRA/all_seq/chip/'