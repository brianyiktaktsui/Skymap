

# [Click here for quick-start to go from data slicing to figures in < 2 minutes](http://hannahcarterlab.org/public-jupyterhub/)


Table of Contents
=================

(Links are clickable if u open the README.ipynb in JupyterNotebook)
  * [Summary](#Summary)
  * [Data directory and loading examples](#Data-directory-and-loading-examples)
      * [-omic data](#-omic-data)
      * [Metadata](#Metadata)
      * [Axulilary](#Axulilary)
  * [Example jupyter notebook analysis using reprocessed data](#Example-jupyter-notebook-analysis-using-reprocessed-data)
      * [1. Locating  variant and correlating with RNAseq and metadata](#Locating-variant-and-correlating-with-RNAseq-and-metadata)
      * [2. High resolution mouse developmental hierachy map](#High-resolution-mouse-developmental-hierachy-map)
      * [3. Simple RNAseq data slicing and hypothesis testing](#Simple-RNAseq-data-slicing-and-hypothesis-testing)
  * [Methods](#Methods)
      * [Slides](#Slides)
  * [Pipeline](#Pipeline)
      * [Metadata: Download, parse and merge SRA META DATA](#SRA-Metadata-download-parse-and-merge)
      * [Allelic read counts](#Allelic-read-counts)
      * [Transcript counting](#Transcript-counting)
      * [Metadata layout axuliary](#Metadata-layout-axuliary)
    * [Acknowledgement](#Acknowledgement)
    * [Data format and coding style](#Data-format-and-coding-style)
  * [References](#References)
      * [Manuscripts in biorxiv related to this project](#Manuscripts-in-biorxiv-related-to-this-project)


**Feel free to contact me @: btsui@eng.ucsd.edu (I will try to reply within 3 days)**

# Summary

Skymap is a standalone database that aims to offer: 
1. **a single data matrix** for each omic layer for each species that spans a total of **>400k sequencing runs** from all the public studies, which is done by reprocessing **petabytes** worth of sequencing data. Here is how much data we have reprocessed from the SRA: 
![alt text](./Figures/sra_data_processed.png)
2. **a biological metadata file** that describe the relationships between the sequencing runs and also the keywords extracted from over **3 million** freetext annotations using NLP. 
3. **a technical metadata file** that describes the relationships between the sequencing runs. 

**Solution: three tables to related > 100k experiments**: 
For examples, all the variant data and the data columns can be interpolated like this: 
![alt text](./Figures/Skymap_SNP_description.png
)

**Where they can all fit into your personal computer.**

[Click here to check out the quick start page and start playing around with the data](https://github.com/brianyiktaktsui/Skymap/blob/master/README.md#quick-start-10-mins)





# quick-installation-10-mins



1. [install miniconda/anaconda with python version >=3.4]( https://conda.io/miniconda.html) (**won't work with python 2**)

2. Copy and paste to run this following line in unix terminal
    * `conda create --yes -n skymap jupyter python=3.6 pandas=0.23.4 && source activate skymap && jupyter-notebook`

3. [Click me to download the examples notebooks](https://github.com/brianyiktaktsui/Skymap/raw/master/ExampleDataLoading.zip) 
4. Choose one of the following notebooks to run. **The code will automatically update your python pandas**, [create a new conda environment if necessary](https://conda.io/docs/user-guide/tasks/manage-environments.html).
   * **loadVariantDataBySRRID.ipynb**: requires 1GB of disk space and 5GB of RAM. 
   * **loadingRNAseqByGene.ipynb**: requires  20GB of disk space and 1GB RAM. 


5. Click "Run All" to execute all the cells. The notebook will download the example data, install the depedencies and run the data query example. 




[Check here for more info on executing jupyter notebook](http://jupyter-notebook-beginner-guide.readthedocs.io/en/latest/execute.html)




**Diagnosis:** 

* If you run into errors from packages, try the versions I used: python v3.6.5,  pandas v0.23.4, synapse client v1.8.1. 
* If sage synapse download fails, download the corresponding python pandas pickle using the web interface instead (https://www.synapse.org/#!Synapse:syn11415602/files/) and read in the pickle using pandas.read_pickle.





# Data directory and loading examples



I tried to keep the loading to be as simple as possible. The jupyter-notebook each have <10 lines of python codes and package dependency on python pandas only. The memory requirement are all less than 5G. 

### -omic data
| Title | Data URL | Jupyter-notebook loading examples | Format | Uses|
| ---: | ----: | ----: | ----:| ---: |
| Loading allelic read counts by SRR (SRA sequencing run) ID | https://www.synapse.org/#!Synapse:syn15624400 | [click me to view](./clean_notebooks/ExampleDataLoading/loadVariantDataBySRRID.ipynb) | python pandas pickle dataframe| Variant, CNV detection|
| Expression matrices| https://www.synapse.org/#!Synapse:syn11415787 | [click me to view](./clean_notebooks/ExampleDataLoading/loadingRNAseqByGene.ipynb)| numpy array|Expression level quantification| 
| Read coverage | - | [availability depending upon demand](http://seqanswers.com/forums/showthread.php?t=83975)| - |  ChIP Peak detection|
|Microbe quantification| - | [availability depending upon demand](http://seqanswers.com/forums/showthread.php?t=83975) | - | Microbiome community detection |


### Metadata

All the metadtata files are located at sage synapse folder: https://www.synapse.org/#!Synapse:syn15661258

| Title | File name | Jupyter-notebook loading examples | Format | 
| ---: | ----: | ----: | ----:|
| biospecieman annotations| allSRS.pickle.gz | [click me to view](./clean_notebooks/ExampleDataLoading/loadInMetaData.ipynb)| python pandas pickle dataframe|
| experimental annotations | allSRX.pickle.gz | [click me to view](./Skymap/blob/master/clean_notebooks/ExampleDataLoading/loadInMetaData.ipynb) | python pandas pickle dataframe|
|biospeiciman experimental and sequencing runs mappings. sequencing and QC stats| sra_dump.fastqc.bowtie_algn.pickle | [click me to view](./Skymap/blob/master/clean_notebooks/ExampleDataLoading/loadInMetaData.ipynb) | python pandas pickle dataframe|

### Axulilary
|Title| File name | 
| ---: | ----: | 
| Distribution of data processed over time | [checkProgress.ipynb](./Pipelines/RNAseq/checkProgress.ipynb) | 
|Generate RNAseq references| [generateReferences.ipynb](./RNAseq/generateReferences.ipynb)|

# Example jupyter notebook analysis using reprocessed data

### Locating variant and correlating with RNAseq and metadata
This is probably the best example that give you an idea on how to go from data slicing in Skymap to basic data analysis. 

[jupyter notebook link](https://github.com/brianyiktaktsui/Skymap/blob/master/XGS_WGS/FindStudiesWithBrafV600Mutated.ipynb)

### High resolution mouse developmental hierachy map
[jupyter notebook link](https://github.com/brianyiktaktsui/Skymap/blob/master/jupyter-notebooks/clean_notebooks/TemporalQuery_V4_all_clean.ipynb
)

Aggregating many studies (node) to form a smooth mouse developmental hierachy map. By integrating the vast amount of public data, we can cover many developmental time points, which sometime we can see a more transient expression dynamics both across tissues and within tissues over developmental time course. 

Each componenet represent a tissue. Each node represent a particular study at a particular time unit. The color is base on the developmental time extracted from experimental annotation using regex. The node size represent the # of sequencing runs in that particulr time point and study. Each edge represent a differentiate-to or part-of relationship.
![alt text](./Figures/heirachy_time.png "Logo Title Text 1")
And you can easily overlay gene expression level on top of it. As an example, Tp53 expression is known to be tightly regulated in development. Let's look at the dynamic of Tp53 expression over time and spatial locations in the following plot.
![alt_text](./Figures/heirachy_Trp53.png "tp53")

### Simple RNAseq data slicing and hypothesis testing
[jupyer notebook link](https://github.com/brianyiktaktsui/Skymap_legacy/blob/master/DataSlicingExample.ipynb)





# Methods 
### Slides 
**Google docs and slides with links pointing to jupyter-notebooks**:
The numbers from the jupyter notebooks will be different from the manuscript as there are more data being incoperated everyday. The hope is that it can help you understand each number and figures from the manuscript. 

|Title| Mansucript URL | Figures URL | 
| ---: | ---: |---: |
|Extracting allelic read counts from 250,000 human sequencing runs in Sequence Read Archive| https://docs.google.com/document/d/1BGGQOpWczOwan9STqs-J9zpa8A-aj4aJ1RND_qKzRFs |https://docs.google.com/presentation/d/1dERUDHh2ab8UdPaHa-ki-8RMae6yi2eYJQM4b7ArVog |
|Meta-analysis using NLP (Metamap) and reprocessed RNAseq data| https://docs.google.com/presentation/d/14vLJJQ6ziw-2aLDoQAJGyv1sYo5ENzljsqsbZr9jNLM| 




| Title | google docs  | google slides |
| ---: | --: | --: | 
| Extracting allelic read counts from 250,000 human sequencing runs in Sequence Read Archive | https://docs.google.com/document/d/1BGGQOpWczOwan9STqs-J9zpa8A-aj4aJ1RND_qKzRFs | https://docs.google.com/presentation/d/1dERUDHh2ab8UdPaHa-ki-8RMae6yi2eYJQM4b7ArVog |





**Unpublished but ongoing manuscripts**

| Title | google doc |
| ---: | --: |
| Meta-analysis using NLP (Metamap) and reprocessed RNAseq data | https://docs.google.com/document/d/1_nES7vroX7lCwf5NSNBVZ1k2iubYm5wLeFqusq5aZuk |  |


#  Pipeline

The way I organized the code is trying to keep the code as simple as possible. 
For each pipeline, it has 6 scripts, <500 lines each to ensure readability. Run each pipeliine starting with calcuate_uprocessed.py, which calculate the number of files still require for processing.



If you happen to want to make a copy of the pipeline: 
* make a copy of the pipeline by cloning this github repo, 

* `conda env create -n environment_conda_py26_btsui --force -f ./conda_envs/environment_conda_py26_btsui.yml`

* `conda env create -n environment_conda_py36_btsui --force -f ./conda_envs/environment_conda_py36_btsui.yml`


* For Python 2 codes, `source activate environment_conda_py26_btsui` before running 

* For Python 3 codes, `source activate environment_conda_py36_btsui` before running 

Repalce my directory (/cellar/users/btsui/Project/METAMAP/code/metamap/)with your directory if you wanna run it. 

Here are the scripts:




### SRA Metadata download parse and merge 



|Steps | Code| Input description|Input dir|Output description|Output dir| Timing| Python version|
|----:| ----:| ----:|----:|----:|----:| ----:|----:|
|download SRAmetadata|[pull_SRA_meta](./Pipelines/Update_SRA_meta_data/pull_SRA_meta.ipynb) |none, download from web||SRA meta data| /nrnb/users/btsui/tmp/SRA_META/| 30 mins| Python 3 |
|parse SRA metadata using Metamap| [parse SRS and SRX metadata](./SRA_META/SRAManager.ipynb) |  SRA files in XML formats|/nrnb/users/btsui/tmp/SRA_META/| list of pandas series containing list of (SRS,attribute, freetext) | /cellar/users/btsui/Data/nrnb01_nobackup/tmp/METAMAP//splittedInput_SRAMangaer_SRA_META/| 20 mins| Python 2| 
|merge SRA metadata | [merge SRS and SRX parsed](./SRA_META/SRAmerge.ipynb)| | list of pandas series containing list of (SRS,attribute, freetext) |/cellar/users/btsui/Data/nrnb01_nobackup/tmp/METAMAP//splittedInput_SRAMangaer_SRA_META/(allSRS.pickle,allSRX.pickle) |all SRA SRS biospecieman annotation in allSRS.pickle and allSRX.pickle  | /cellar/users/btsui/Data/nrnb01_nobackup/METAMAP/ | 10 mins| Python 3|
|annotate SRA meta data based on SRX parsed | [annotate SRA data](./Pipelines/Update_SRA_meta_data/annotate_SRA_meta_data.ipynb) |
| |[upload meta data to AWS](Pipelines/Update_SRA_meta_data/upload_AWS.ipynb)|




Input directory


```python
!ls -lath /nrnb/users/btsui/tmp/ 
```

    total 15G
    drwxr-xr-x 930873 btsui users          32M Jul 24 21:16 SRA_META
    drwxr-xr-x      6 btsui users          512 Jan  4  2018 .
    drwxr-xr-x      6 btsui CarterGeneral  512 Aug 10  2016 ..
    -rw-r--r--      1 btsui users          15G Jul  4  2016 NCBI_SRA_Metadata_Full_20160702_Run_2.tar
    drwxr-xr-x     11 btsui users         128K Oct  2  2015 METAMAP
    drwxr-xr-x      3 btsui users          512 Aug 31  2015 TSCC
    drwxr-xr-x      2 btsui users         128K Aug 12  2015 bioSample


Output directory


```python
!ls -lath /data/cellardata/users/btsui/SRA/DUMP/
```

    total 4.3G
    -rw-r--r--  1 btsui users  21M Oct  8 19:31 allSRS.with_processed_data.pickle.gz
    drwxr-xr-x  3 btsui users   15 Oct  8 19:30 .
    -rw-r--r--  1 btsui users 212M Aug 28 18:31 sra_dump.csv.gz
    -rw-r--r--  1 btsui users 556M Jul 24 20:13 SRA_Run_Members.tab
    -rw-r--r--  1 btsui users 1.9G Jul 24 20:13 NCBI_SRA_Metadata_Full_20180702.tar.gz
    -rw-r--r--  1 btsui users 4.0G Jul 24 20:13 SRA_Accessions.tab
    -rw-r--r--  1 btsui users 659M Jul 21 12:11 sra_dump.fastqc.bowtie_algn.pickle
    -rw-r--r--  1 btsui users 139M Jul 19 18:52 merged_variant_aligning_statistics.tsv
    -rw-r--r--  1 btsui users 372M May 16 08:08 sra_dump.pickle
    drwxr-xr-x 13 btsui users   14 Mar  1  2018 ..
    drwxr-xr-x  3 btsui users    3 Jan  5  2018 FULL_SRA_meta
    -rw-r--r--  1 btsui users 133M Jan  5  2018 allSRX.pickle.gz
    -rw-r--r--  1 btsui users 241M Jan  5  2018 allSRS.pickle.gz
    -rw-r--r--  1 btsui users 175M Oct 30  2017 file_meta.txt
    -rw-r--r--  1 btsui users 175M Oct 30  2017 meta.txt



### Allelic read counts
|Pipeline | Code| 
|---- | ----|
|SNP extraction | ./Pipelines/snp/calculate_unprocessed.py|
|merge SNP alignment statistics | [merge_variant_aligning_statistics](./Analysis/merge_variant_aligning_statistics.ipynb) |
| merge SNP data | [merge SNP data into pandas pickles](./Pipelines/snp/Merge/calculate_unprocessed.ipynb) |


Details of benchmarking against TCGA are located at: 

http://localhost:6001/notebooks/Project/METAMAP/notebook/RapMapTest/XGS_WGS/README_TCGA_benchmark.ipynb

However, due to the fact where patients allele informations are protected, we are not providing the allellic read counts for TCGA. 




### Transcript counting

| Pipeline Code| 
|---- | 
|./Pipelines/RNAseq/calculate_unprocessed.py |
| [merge RNAseq data into transcripts](./Pipelines/RNAseq/merge/mergeKallistoOutputIntoTranscript.ipynb)|
| [reduce transcripts count to gene count using sum ](./Pipelines/RNAseq/merge/reduceToGeneLevel.ipynb)|
|[merge data into single numpy mmap matrix ](./Pipelines/RNAseq/merge/mergeGeneMatrix.ipynb)
| [upload expression data to AWS (On this step now)](./Pipelines/RNAseq/merge/upload_AWS.ipynb)|

|Auxilary Code|
|---- | 
| [file count](./Pipelines/RNAseq/merge/fileCount.ipynb)|
| [merge Kalististo mapping stats](./Pipelines/RNAseq/merge/mergeKalistoMappingStats.ipynb)|

Intermediate files


```python
ls -lath /nrnb/users/btsui/Data/all_seq/rnaseq_merged_chunks/  | head
```

    total 566G
    -rw-r--r--  1 btsui users   76M Oct 12 09:32 Mus_musculus.gene_symbol.tpm.SRR3.pickle
    -rw-r--r--  1 btsui users   96M Oct 12 09:32 Mus_musculus.gene_symbol.tpm.ERR2.pickle
    -rw-r--r--  1 btsui users   75M Oct 12 09:32 Homo_sapiens.gene_symbol.tpm.SRR27.pickle
    -rw-r--r--  1 btsui users  9.4M Oct 12 09:32 Drosophila_melanogaster.gene_symbol.est_counts.ERR1.pickle
    drwxr-xr-x  2 btsui users  128K Oct 12 09:32 [0m[01;34m.[0m/
    -rw-r--r--  1 btsui users  263M Oct 12 09:32 Mus_musculus.gene_symbol.est_counts.SRR25.pickle
    -rw-r--r--  1 btsui users  836M Oct 12 09:32 Homo_sapiens.gene_symbol.est_counts.SRR39.pickle
    -rw-r--r--  1 btsui users   17M Oct 12 09:32 Drosophila_melanogaster.gene_symbol.est_counts.SRR36.pickle
    -rw-r--r--  1 btsui users  253M Oct 12 09:32 Homo_sapiens.gene_symbol.est_counts.SRR5.pickle
    ls: write error


Output files


```python
!ls -lath /nrnb/users/btsui/Data/all_seq/rnaseq_merged/ 
```

    total 317G
    -rw-r--r--  1 btsui users 139M Oct  8 19:43 merged_kallisto_run_info.pickle
    drwxr-xr-x  2 btsui users 128K Sep 13 08:32 .
    -rw-r--r--  1 btsui users  25G Aug 29 12:25 Mus_musculus.transcript.tpm.npy
    -rw-r--r--  1 btsui users 8.0G Aug 29 12:25 Mus_musculus.transcript.tpm.npy.gz
    -rw-r--r--  1 btsui users 1.3M Aug 29 12:24 Mus_musculus.transcript.tpm.columns.txt
    -rw-r--r--  1 btsui users 2.2M Aug 29 12:24 Mus_musculus.transcript.tpm.index.txt
    -rw-r--r--  1 btsui users  46G Aug 29 12:21 Mus_musculus.transcript.est_counts.npy
    -rw-r--r--  1 btsui users 9.5G Aug 29 12:21 Mus_musculus.transcript.est_counts.npy.gz
    -rw-r--r--  1 btsui users 2.4M Aug 29 12:20 Mus_musculus.transcript.est_counts.columns.txt
    -rw-r--r--  1 btsui users 2.2M Aug 29 12:20 Mus_musculus.transcript.est_counts.index.txt
    -rw-r--r--  1 btsui users  62G Aug 29 12:14 Homo_sapiens.transcript.tpm.npy
    -rw-r--r--  1 btsui users  21G Aug 29 12:14 Homo_sapiens.transcript.tpm.npy.gz
    -rw-r--r--  1 btsui users 2.1M Aug 29 12:13 Homo_sapiens.transcript.tpm.columns.txt
    -rw-r--r--  1 btsui users 2.7M Aug 29 12:13 Homo_sapiens.transcript.tpm.index.txt
    -rw-r--r--  1 btsui users  13G Aug 29 12:09 Homo_sapiens.gene_symbol.tpm.npy
    -rw-r--r--  1 btsui users 5.4G Aug 29 12:09 Homo_sapiens.gene_symbol.tpm.npy.gz
    -rw-r--r--  1 btsui users 2.1M Aug 29 12:08 Homo_sapiens.gene_symbol.tpm.columns.txt
    -rw-r--r--  1 btsui users 268K Aug 29 12:08 Homo_sapiens.gene_symbol.tpm.index.txt
    -rw-r--r--  1 btsui users  62G Aug 29 12:05 Homo_sapiens.transcript.est_counts.npy
    -rw-r--r--  1 btsui users  13G Aug 29 12:05 Homo_sapiens.transcript.est_counts.npy.gz
    -rw-r--r--  1 btsui users 2.1M Aug 29 12:04 Homo_sapiens.transcript.est_counts.columns.txt
    -rw-r--r--  1 btsui users 2.7M Aug 29 12:04 Homo_sapiens.transcript.est_counts.index.txt
    -rw-r--r--  1 btsui users  50G Aug 29 11:52 Homo_sapiens.gene_symbol.est_counts.npy
    -rw-r--r--  1 btsui users 5.4G Aug 29 11:52 Homo_sapiens.gene_symbol.est_counts.npy.gz
    -rw-r--r--  1 btsui users 2.1M Aug 29 11:51 Homo_sapiens.gene_symbol.est_counts.columns.txt
    -rw-r--r--  1 btsui users 268K Aug 29 11:51 Homo_sapiens.gene_symbol.est_counts.index.txt
    drwxr-xr-x 18 btsui users 128K Aug 29 10:41 ..
    -rw-r--r--  1 btsui users 502K Aug 28 20:25 Danio_rerio.gene_symbol.est_counts.npy
    -rw-r--r--  1 btsui users   99 Aug 28 20:25 Danio_rerio.gene_symbol.est_counts.columns.txt
    -rw-r--r--  1 btsui users 221K Aug 28 20:25 Danio_rerio.gene_symbol.est_counts.index.txt
    -rw-r--r--  1 btsui users 252K Aug 28 20:25 Danio_rerio.gene_symbol.est_counts.npy.gz
    -rw-r--r--  1 btsui users 762K Aug 28 20:24 Canis_familiaris.gene_symbol.tpm.npy
    -rw-r--r--  1 btsui users  285 Aug 28 20:24 Canis_familiaris.gene_symbol.tpm.columns.txt
    -rw-r--r--  1 btsui users  94K Aug 28 20:24 Canis_familiaris.gene_symbol.tpm.index.txt
    -rw-r--r--  1 btsui users 129K Aug 28 20:24 Canis_familiaris.gene_symbol.tpm.npy.gz
    -rw-r--r--  1 btsui users 3.0M Aug 28 20:24 Canis_familiaris.gene_symbol.est_counts.npy
    -rw-r--r--  1 btsui users  285 Aug 28 20:24 Canis_familiaris.gene_symbol.est_counts.columns.txt
    -rw-r--r--  1 btsui users  94K Aug 28 20:24 Canis_familiaris.gene_symbol.est_counts.index.txt
    -rw-r--r--  1 btsui users 136K Aug 28 20:24 Canis_familiaris.gene_symbol.est_counts.npy.gz
    -rw-r--r--  1 btsui users 1.9M Aug 28 19:59 Canis_familiaris.transcript.tpm.pickle
    -rw-r--r--  1 btsui users 295K Aug 28 19:59 Canis_familiaris.transcript.tpm.pickle.gz
    -rw-r--r--  1 btsui users 1.9M Aug 28 19:50 Canis_familiaris.transcript.est_counts.pickle
    -rw-r--r--  1 btsui users 239K Aug 28 19:50 Canis_familiaris.transcript.est_counts.pickle.gz
    -rw-r--r--  1 btsui users 2.2M Aug 28 18:55 Danio_rerio.transcript.est_counts.pickle


### Coverage
|Code|
|---|
| [calculating reads coverage](./Pipelines/chip/calculate_unprocessed.py)|


### Metadata layout axuliary
|Column | meaning|
|: ---: | :---|
| new_ScientificName | the string which the pipeline will use for matching with the reference genome as the species
| ScientificName | original scientific name extracted from NCBI SRS| 

## Acknowledgement


Please considering citing if you are using Skymap. (https://www.biorxiv.org/content/early/2018/08/07/386441)

We want to thank for the advice and resources from Dr. Hannah Carter (my PI), Dr. Jill Mesirov, Dr. Trey Ideker and Shamin Mollah. We also want to thank Dr. Ruben Arbagayen, Dr. Nate Lewis for their suggestion. 
The method will soon be posted in bioarchive. Also, we want to thank the Sage Bio Network for hosting the data. We also thank to thank the NCBI for holding all the published raw reads at  [Sequnece Read Archive](https://www.ncbi.nlm.nih.gov/sra). 

There are also many people who help tested Skymap: Ben Kellman, Rachel Marty, Daniel Carlin, Spiko van Dam. 

Grant money that make this work possible: NIH DP5OD017937,GM103504

Term of use: Use Skymap however you want. Just dont sue me, I have no money. 


For why I named it Skymap, I forgot.

## Data format and coding style

The storage is in python pandas pickle format. Therefore, the only packges you need to load in the data is numpy and pandas, the backbone of data analysis in python. We keep the process of data loading as lean as possible. Less code means less bugs and less errors. For now, Skymap is geared towards ML/data science folks who are hungry for the vast amount of data and ain't afraid of coding. I will port the data to native HDF5 format to reduce platform dependency once I get a chance. 

I tried to keep the code and parameters to be lean and self-explanatory for your reference. 



# References
**ISMB 2018 poster:** https://github.com/brianyiktaktsui/Skymap/blob/master/ISMB_poster_Skymap.pdf	

**Preprint on allelic read counts:** https://www.synapse.org/#!Synapse:syn11415602/files/

**Data:** https://www.synapse.org/#!Synapse:syn11415602/files/

### Manuscripts in biorxiv related to this project
| Title | URL to manuscript | github|  
| ---: | ---: | ---: | 
| Extracting allelic read counts from 250,000 human sequencing runs in Sequence Read Archive| https://www.biorxiv.org/content/biorxiv/early/2018/08/07/386441.full.pdf | |
| Deep biomedical named entity recognition NLP engine | https://www.biorxiv.org/content/early/2018/09/12/414136 | https://github.com/brianyiktaktsui/DEEP_NLP |






```python
!ls -lath /nrnb/users/btsui/Data/merged/snp/hg38/mergedBySRR_smallerChunk/  |head 
```

    total 59G
    drwxr-xr-x 2 btsui users  128K Oct  4 14:15 .
    -rw-r--r-- 1 btsui users  3.8M Oct  4 14:15 1581000.pickle.gz
    -rw-r--r-- 1 btsui users  8.6M Oct  4 14:15 1558000.pickle.gz
    -rw-r--r-- 1 btsui users  822K Oct  4 14:15 1524000.pickle.gz
    -rw-r--r-- 1 btsui users  760K Oct  4 14:15 1543000.pickle.gz
    -rw-r--r-- 1 btsui users  2.3M Oct  4 14:15 1572000.pickle.gz
    -rw-r--r-- 1 btsui users  3.7M Oct  4 14:15 1589000.pickle.gz
    -rw-r--r-- 1 btsui users  726K Oct  4 14:15 1590000.pickle.gz
    -rw-r--r-- 1 btsui users  3.4M Oct  4 14:15 1520000.pickle.gz
    ls: write error: Broken pipe

