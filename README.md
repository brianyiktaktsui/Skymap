
Table of Contents
=================

  * [Summary](#summary)
  * [Quick start (&lt;10 mins)](#quick-start-10-mins)
  * [Data directory and data loading examples](#data-directory-and-data-loading-examples)
      * [-omic data](#-omic-data)
      * [Metadata](#metadata)
      * [Axulilary](#axulilary)
  * [Example jupyter notebook analysis using reprocessed data](#example-jupyter-notebook-analysis-using-reprocessed-data)
      * [1. Locating  variant and correlating with RNAseq and metadata](#1-locating--variant-and-correlating-with-rnaseq-and-metadata)
      * [2. High resolution mouse developmental hierachy map](#2-high-resolution-mouse-developmental-hierachy-map)
      * [3. Simple RNAseq data slicing and hypothesis testing](#3-simple-rnaseq-data-slicing-and-hypothesis-testing)
  * [Methods](#methods)
      * [Slides](#slides)
    * [Pipeline](#pipeline)
      * [Metadata: Download, parse and merge SRA META DATA](#metadata-download-parse-and-merge-sra-meta-data)
      * [Allelic read counts](#allelic-read-counts)
      * [Transcript counting](#transcript-counting)
      * [Metadata layout axuliary](#metadata-layout-axuliary)
    * [Acknowledgement](#acknowledgement)
    * [Data format and coding style](#data-format-and-coding-style)
  * [References](#references)
      * [Manuscripts in biorxiv related to this project](#manuscripts-in-biorxiv-related-to-this-project)


**Feel free to contact me @: btsui@eng.ucsd.edu (I will try to reply within 3 days)**

# Summary

Skymap is a standalone database that aims to offer: 
1. **a single data matrix** for each omic layer for each species that spans **>200k sequencing runs** from all the public studies, which is done by reprocessing **petabytes** worth of sequencing data. Here is how much data we have reprocessed from the SRA: 
![alt text](./Figures/sra_data_processed.png)
2. **a biological metadata file** that describe the relationships between the sequencing runs and also the keywords extracted from over **3 million** freetext annotations using NLP. 
3. **a technical metadata file** that describes the relationships between the sequencing runs. 

**Solution: three tables to related > 100k experiments**: 
For examples, all the variant data and the data columns can be interpolated like this: 
![alt text](./Figures/Skymap_SNP_description.png
)

**Where they can all fit into your personal computer.**

[Click here to check out the quick start page and start playing around with the data](https://github.com/brianyiktaktsui/Skymap/blob/master/README.md#quick-start-10-mins)


# Quick start (<10 mins)



1. [install anaconda with python version >=3.4]( https://www.anaconda.com/download/) (**won't work with python 2**)
copy paste and run this line in unix terminal
    * `conda create --yes -n skymap jupyter python=3.6 pandas=0.23.4 && source activate skymap && jupyter-notebook`

2. [Click me to download the examples notebooks](https://github.com/brianyiktaktsui/Skymap/raw/master/ExampleDataLoading.zip) 
3. Choose one of the following notebooks to run. **The code will automatically update your python pandas**, [create a new conda environment if necessary](https://conda.io/docs/user-guide/tasks/manage-environments.html).
   * **loadVariantDataBySRRID.ipynb**: requires 1GB of disk space and 5GB of RAM. 
   * **loadingRNAseqByGene.ipynb**: requires  20GB of disk space and 1GB RAM. 


4. Click "Run All" to execute all the cells. The notebook will download the example data, install the depedencies and run the data query example. 




[Check here for more info on executing jupyter notebook](http://jupyter-notebook-beginner-guide.readthedocs.io/en/latest/execute.html)




**Diagnosis:** 

* If you run into errors from packages, try the versions I used: python v3.6.5,  pandas v0.23.4, synapse client v1.8.1. 
* If sage synapse download fails, download the corresponding python pandas pickle using the web interface instead (https://www.synapse.org/#!Synapse:syn11415602/files/) and read in the pickle using pandas.read_pickle.





# Data directory and data loading examples



I tried to keep the loading to be as simple as possible. The jupyter-notebook each have <10 lines of python codes and package dependency on python pandas only. The memory requirement are all less than 5G. 

### -omic data
| Title | Data URL | Jupyter-notebook loading examples | Format | Uses|
| ---: | ----: | ----: | ----:| ---: |
| Loading allelic read counts by SRR (SRA sequencing run) ID | https://www.synapse.org/#!Synapse:syn15624400 | [click me to view](https://github.com/brianyiktaktsui/Skymap/blob/master/clean_notebooks/ExampleDataLoading/loadVariantDataBySRRID.ipynb) | python pandas pickle dataframe| Variant, CNV detection|
| Expression matrices| https://www.synapse.org/#!Synapse:syn11415787 | [click me to view](https://github.com/brianyiktaktsui/Skymap/blob/master/clean_notebooks/ExampleDataLoading/loadingRNAseqByGene.ipynb)| numpy array|Expression level quantification| 
| Read coverage | - | [availability depending upon demand](http://seqanswers.com/forums/showthread.php?t=83975)| - |  ChIP Peak detection|
|Microbe quantification| - | [availability depending upon demand](http://seqanswers.com/forums/showthread.php?t=83975) | - | Microbiome community detection |


### Metadata

All the metadtata files are located at sage synapse folder: https://www.synapse.org/#!Synapse:syn15661258

| Title | File name | Jupyter-notebook loading examples | Format | 
| ---: | ----: | ----: | ----:|
| biospecieman annotations| allSRS.pickle.gz | [click me to view](https://github.com/brianyiktaktsui/Skymap/blob/master/clean_notebooks/ExampleDataLoading/loadInMetaData.ipynb)| python pandas pickle dataframe|
| experimental annotations | allSRX.pickle.gz | [click me to view](https://github.com/brianyiktaktsui/Skymap/blob/master/clean_notebooks/ExampleDataLoading/loadInMetaData.ipynb) | python pandas pickle dataframe|
|biospeiciman experimental and sequencing runs mappings. sequencing and QC stats| sra_dump.fastqc.bowtie_algn.pickle | [click me to view](https://github.com/brianyiktaktsui/Skymap/blob/master/clean_notebooks/ExampleDataLoading/loadInMetaData.ipynb) | python pandas pickle dataframe|

### Axulilary
|Title| File name | 
| ---: | ----: | 
| Distribution of data processed over time | [checkProgress.ipynb](https://github.com/brianyiktaktsui/Skymap/blob/master/Pipelines/RNAseq/checkProgress.ipynb) | 
|Generate RNAseq references| [generateReferences.ipynb](./RNAseq/generateReferences.ipynb)|

# Example jupyter notebook analysis using reprocessed data

### 1. Locating  variant and correlating with RNAseq and metadata
This is probably the best example that give you an idea on how to go from data slicing in Skymap to basic data analysis. 

[jupyter notebook link](https://github.com/brianyiktaktsui/Skymap/blob/master/XGS_WGS/FindStudiesWithBrafV600Mutated.ipynb)

### 2. High resolution mouse developmental hierachy map
[jupyter notebook link](https://github.com/brianyiktaktsui/Skymap/blob/master/jupyter-notebooks/clean_notebooks/TemporalQuery_V4_all_clean.ipynb
)

Aggregating many studies (node) to form a smooth mouse developmental hierachy map. By integrating the vast amount of public data, we can cover many developmental time points, which sometime we can see a more transient expression dynamics both across tissues and within tissues over developmental time course. 

Each componenet represent a tissue. Each node represent a particular study at a particular time unit. The color is base on the developmental time extracted from experimental annotation using regex. The node size represent the # of sequencing runs in that particulr time point and study. Each edge represent a differentiate-to or part-of relationship.
![alt text](./Figures/heirachy_time.png "Logo Title Text 1")
And you can easily overlay gene expression level on top of it. As an example, Tp53 expression is known to be tightly regulated in development. Let's look at the dynamic of Tp53 expression over time and spatial locations in the following plot.
![alt_text](./Figures/heirachy_Trp53.png "tp53")

### 3. Simple RNAseq data slicing and hypothesis testing
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
| Deep biomedical named entity recognition NLP engine | https://docs.google.com/document/d/1sbm9L8-OCVZ_qoPqwZyedE5uL4I9k0Hg7znZn6El_l0 | https://github.com/brianyiktaktsui/DEEP_NLP |

##  Pipeline

The way I organized the code is trying to keep the code as simple as possible. 
For each pipeline, it has 6 scripts, <500 lines each to ensure readability. Run each pipeliine starting with calcuate_uprocessed.py, which calculate the number of files still require for processing.

If you happen to want to dig into the gut and gore, and make a copy of the pipeline, here are the scripts:




### Metadata: Download, parse and merge SRA META DATA

|Steps | Code| Input description|Input dir|Output description|Output dir| Timing| Python version|
|----:| ----:| ----:|----:|----:|----:| ----:|----:|
|download SRAmetadata|[pull_SRA_meta](./Pipelines/Update_SRA_meta_data/pull_SRA_meta.ipynb) |none, download from web||SRA meta data| /nrnb/users/btsui/tmp/SRA_META/| 30 mins| Python 3 |
|parse SRA metadata | [parse SRS and SRX metadata](./SRA_META/SRAManager.py) |  SRA files in XML formats|/nrnb/users/btsui/tmp/SRA_META/| list of pandas series containing list of (SRS,attribute, freetext) | /cellar/users/btsui/Data/nrnb01_nobackup/tmp/METAMAP//splittedInput_SRAMangaer_SRA_META/| 20 mins| Python 2| 
|merge SRA metadata | [merege SRS and SRX parsed](./SRA_META/SRAmerge.py)| | list of pandas series containing list of (SRS,attribute, freetext) |/cellar/users/btsui/Data/nrnb01_nobackup/tmp/METAMAP//splittedInput_SRAMangaer_SRA_META/(allSRS.pickle,allSRX.pickle) |all SRA SRS biospecieman annotation in allSRS.pickle and allSRX.pickle  | /cellar/users/btsui/Data/nrnb01_nobackup/METAMAP/ | 10 mins| Python 3|
|annotate SRA meta data based on SRX parsed | [annotate SRA data](./Pipelines/Update_SRA_meta_data/annotate_SRA_meta_data.ipynb) |

Repalce my directory (/cellar/users/btsui/Project/METAMAP/code/metamap/)with your directory if you wanna run it. 


### Allelic read counts
|Pipeline | Code| 
|---- | ----|
|SNP extraction | ./Pipelines/snp/calculate_unprocessed.py|
|calculating reads coverage | ./Pipelines/chip/calculate_unprocessed.py|
|merge SNP alignment statistics | [merge_variant_aligning_statistics](./Analysis/merge_variant_aligning_statistics.ipynb) |
| merge SNP data | [merge SNP data into pandas pickles](./XGS_WGS/ParseAndMergeBamReadCount.ipynb) |


Details of benchmarking against TCGA are located at: 

http://localhost:6001/notebooks/Project/METAMAP/notebook/RapMapTest/XGS_WGS/README_TCGA_benchmark.ipynb

However, due to the fact where patients allele informations are protected, we are not providing the allellic read counts for TCGA. 




### Transcript counting

|Pipeline | Code| 
|---- | ----|
|RNAseq quantification| ./Pipelines/RNAseq/calculate_unprocessed.py |
|merge RNAseq data| [merge RNAseq data into transcripts](./Pipelines/RNAseq/merge/mergeKallistoOutputIntoTranscript.ipynb)|
|reduce to gene symbol level| [reduce transcripts count to gene count using sum](./Pipelines/RNAseq/merge/reduceToGeneLevel.ipynb)|
|merge into single file| [merge data into single numpy mmap matrix](./Pipelines/RNAseq/merge/mergeGeneMatrix.ipynb)
| | [upload expression data to synapse](./Pipelines/RNAseq/merge/upload.ipynb)|
|file count | [file count](./Pipelines/RNAseq/merge/fileCount.ipynb)

### Metadata layout axuliary
|Column | meaning|
|: ---: | :---|
| new_ScientificName | the string which the pipeline will use for matching with the reference genome as the species
| ScientificName | original scientific name extracted from NCBI SRS| 

## Acknowledgement


Please considering citing if you are using Skymap. (https://www.biorxiv.org/content/early/2018/08/07/386441)

Acknowledgement: We want to thank for the advice and resources from Dr. Hannah Carter (my PI), Dr. Jill Mesirov, Dr. Trey Ideker and Shamin Mollah. We also want to thank Dr. Ruben Arbagayen, Dr. Nate Lewis for their suggestion. 
The method will soon be posted in bioarchive. Also, we want to thank the Sage Bio Network for hosting the data. We also thank to thank the NCBI for holding all the published raw reads at  [Sequnece Read Archive](https://www.ncbi.nlm.nih.gov/sra). 

There are also many people who help tested Skymap: Ben Kellman, Rachel Marty, Daniel Carlin. 

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

