
# TO UPDATE META DATA


|Step | Code| Input description|Input dir|Output description|Output dir| Timing|
|:---------|:---------|------:|---:|
|download SRA metadata | ./Pipelines/Update_SRA_meta_data/pull_SRA_meta.ipynb|none, download from web||SRA meta data| /nrnb/users/btsui/tmp/SRA_META/| 30 mins|
|parse SRA metadata | ./SRA_META/SRAManager.py |  SRA files in XML formats|/nrnb/users/btsui/tmp/SRA_META/| list of pandas series containing list of (SRS,attribute, freetext) | /cellar/users/btsui/Data/nrnb01_nobackup/tmp/METAMAP//splittedInput_SRAMangaer_SRA_META/| 20 mins
|merge SRA metadata | ./SRA_META/SRAmerge.py | list of pandas series containing list of (SRS,attribute, freetext) |/cellar/users/btsui/Data/nrnb01_nobackup/tmp/METAMAP//splittedInput_SRAMangaer_SRA_META/(allSRS.pickle,allSRX.pickle) |all SRA SRS biospecieman annotation in allSRS.pickle and allSRX.pickle  | /cellar/users/btsui/Data/nrnb01_nobackup/METAMAP/ | 10 mins| 



```python
#!cp /cellar/users/btsui/Project/METAMAP/code/metamap/*  ./SRA_META/.
```


```python
#!cat ./SRA_META/SRAManager.py 
```

# Update moelcular data



##  RNAseq
 changed shared variable for each specie: sharedVariable.py

**code**: /cellar/users/btsui/Documents/ipythonNotebook/current_working_dir/GoogleGEO/Job/mpiJob/isoformCounting.py

pipelines: 

http://localhost:6001/tree/Project/METAMAP/notebook/RapMapTest/Pipelines/snp

###### merge
http://localhost:6001/notebooks/Project/METAMAP/notebook/UpdatePipeline/mergeAllRNASeq.ipynb (need update)
Runninng with (EffectiveLength)


##### UPDATE: # of reads 

**code**: http://localhost:6001/notebooks/METAMAP/notebook/UpdatePipeline/calculate_aligned_reads.ipynb

**input**: /cellar/users/btsui/Data/SRA/realigned_DATA_V9_LOG/{specie}/*.lines.log

**output**: /cellar/users/btsui/Data/SRA/realigned_DATA_V9_LOG/n_reads.pickle

## SNP
pipeline

**code** /cellar/users/btsui/Project/METAMAP/notebook/RapMapTest/Pipelines/snp/calculate_unprocessed.py

merge all the parse reads counts data  (time, start: 11:19am, end: )

**code** http://localhost:6001/notebooks/Project/METAMAP/notebook/RapMapTest/XGS_WGS/ParseBamReadCount_base_case.ipynb

## Chip seq
pipeline 

**code** /cellar/users/btsui/Project/METAMAP/notebook/RapMapTest/Pipelines/chip/calculate_unprocessed.py



### Upload data to synapse
http://localhost:6001/notebooks/METAMAP/notebook/UpdatePipeline/CopyMetaData_V2.ipynb
http://localhost:6001/notebooks/Project/METAMAP/notebook/UpdatePipeline/CopyMatrices_v2.ipynb
http://localhost:6001/notebooks/Project/METAMAP/notebook/UpdatePipeline/UploadDataToSynapse.ipynb


#### UPDATE META data with alignment stats: # of number reads. 

**code** http://localhost:6001/notebooks/METAMAP/notebook/UpdatePipeline/UpdateSRAMetaData.ipynb

**deployment**: /cellar/users/btsui/Data/METAMAP/deploy_ready/syn11415787/
#####  Example of data slice
#/cellar/users/btsui/Data/METAMAP/deploy_ready/syn11415787
#### 
http://localhost:6001/notebooks/METAMAP/notebook/Statistics_Key/Code/QueryData/DataSlicingExample.ipynb

### output
/nrnb/users/btsui/Data/all_seq/rnaseq/

### LEGACY




### 3.1 Merge the meta data into a single file

**code** http://localhost:6001/notebooks/Project/METAMAP/notebook/RapMapTest/Pipelines/Update_SRA_meta_data/annotate_SRA_meta_data.ipynb

### 3.2 Format the raw text meta data for NLP parsing 

(20 mins)
**code** http://localhost:6001/notebooks/Project/METAMAP/notebook/RapMapTest/Pipelines/Update_SRA_meta_data/ExportForMetamap.ipynb
input: allSRS.pickle
output: allAttrib.v\d.csv


### 4. Run metamap 
/cellar/users/btsui/Project/METAMAP/code/metamap/clusterRun.py
input: /cellar/users/btsui/Data/nrnb01_nobackup/METAMAP/input/allAttrib.v4.csv
output: allAttrib.v\d.csv.pyc

### 5. Run metamap parsing

6. Reduce the NCIT terms into something simpler

**code** http://localhost:6001/notebooks/Project/METAMAP/notebook/RapMapTest/Pipelines/Update_SRA_meta_data/NCIMetaDataMapping_stemness_V7_NoAnalyis.ipynb

**input** /cellar/users/btsui/Data/nrnb01_nobackup/METAMAP/input/allAttrib.v4.csv.pyc

**output** /cellar/users/btsui/Project/METAMAP/notebook/MapAnnotationToNCI/./MappingData/parent_filtered_NciDf.csv

