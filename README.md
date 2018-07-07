
# In short
Skymap is a standalone database that offers: 
1. **a single data matrix** for each omic layer for each species that [spans >200k sequencing runs from all the public studies](https://www.ncbi.nlm.nih.gov/sra), which is done by reprocessing **petabytes** worth of sequencing data. Here is how much published data are out there: 
![alt text](./Figures/sra_data_availability.png "Logo Title Text 1")

2. **a biological metadata file** that describe the relationships between the sequencing runs and also the keywords extracted from over **3 million** freetext annotations using NLP. 
3. **a techinical metadata file** that describe the relationships between the sequencing runs. 


**Where they can all fit into your personal computer.**

**If you intend to run the examples, please first download the data from here:** https://www.synapse.org/skymap (take < 3 minutes to set up the account). 

Table of Contents
=================

* [In long](#in-long)
  * [Motivation: Pooling processed data from multiple studies is time\-consuming:](#motivation-pooling-processed-data-from-multiple-studies-is-time-consuming)
  * [Solution: An automated pipeline to generate a single data matrix that does simple counting for each specie and omic layer](#solution-an-automated-pipeline-to-generate-a-single-data-matrix-that-does-simple-counting-for-each-specie-and-omic-layer)
  * [Why Skymap while there are so many groups out there also trying to unify the public data](#why-skymap-while-there-are-so-many-groups-out-there-also-trying-to-unify-the-public-data)
  * [Why Skymap offer a local copy instead of a web api](#why-skymap-offer-a-local-copy-instead-of-a-web-api)
  * [Data format and coding style](#data-format-and-coding-style)
* [Data slicing example](#data-slicing-example)
    * [Accessing allelic read count dataframe](#accessing-allelic-read-count-dataframe)
    * [Accessing RNAseq dataframe](#accessing-rnaseq-dataframe)
    * [Accesing biological metadata dataframe](#accesing-biological-metadata-dataframe)
    * [Accessing technical metadata dataframe](#accessing-technical-metadata-dataframe)
* [More examples on using simple code to analyze big data](#more-examples-on-using-simple-code-to-analyze-big-data)
  * [High resolution mouse developmental hierachy map](#high-resolution-mouse-developmental-hierachy-map)
  * [Locating  SNP and correlating with different data layers](#locating--snp-and-correlating-with-different-data-layers)
  * [Simple RNAseq data slicing and hypothesis testing](#simple-rnaseq-data-slicing-and-hypothesis-testing)
  * [Acknowledgement](#acknowledgement)




# In long
## Motivation: Pooling processed data from multiple studies is time-consuming: 
When I first started in bioinformatic couple years ago, I spent much of my time doing two things: 1.) cleaning omic data matrices, e.g. mapping between gene IDs (hgnc, enseml, ucsc, etc.) for processed data matrices, trying all sort of different bioinformatics pipelines that yield basically the same results, investigating what is the exact unit being counted over when pulling pre-processed data from public database, etc.  2.) cleaning metadata annotation, which usually involves extracting and aliasing the labels to the exact same categories. 


This question came to my mind: Can we merge and reduce the petabytes worth of raw reads into a single table that: 1.) captures the commonly used information which can 2.) also fit in your hard drive (<500Gb)? 

## Solution: An automated pipeline to generate a single data matrix that does simple counting for each specie and omic layer 
What I am offering in here is a metadata table and a single data matrix for each omic layer that encapsulate majority of the public data out there by continuously pulling data from [Sequence Read Archive](https://www.ncbi.nlm.nih.gov/sra), a place that host the bulk of the published sequencing data. I believe that "Science started with counting" (from "Cancer: Emperor of all malady" by Siddhartha Mukherjee), and thus I offer counts for all the features: 1. ) the  base resolution ACGT counts for over 200k experiments among NCBI curated SNPs, where read depth and allelic fraction are usually the main drivers for SNP calling. We also offer an expression matrix, which counts at both transcript and gene resolution. With the raw counts, you can normalize however you want. 
The metadata table consists of controlled vocabulary (NCI Terminology) from free text experiment annotations. I used the NLM metamap engine for extracting keywords from freetext. The nice thing is that the UMLS ecosystem from NLM allow the IDs (Concept Unique Identifiers) to be mapped onto different ontologies to relate the terms. NCIT is by far the cleanest general purpose ontology I have seen, low term redundancy, encode medical knowledge from many domains and is well maintained.  
The pipeline in here is trying to suit the needs of the common use cases. In another word, most pipelines out there are more like sport cars, having custom flavors for a specific group of drivers. What I am trying to create is more like a train system, aiming to suit most needs. Unfortunately, if you have more specific requirements, what I am offering is probably not going to work. 


Here are the overview slides for the overall processes of [allelic read counts extraction over 300k known SNPs](https://docs.google.com/presentation/d/1KcumgtLfCdHNnIwkbU5DaQ7UNKHGbJ_fJZFy1cj53yE/edit#slide=id.p3), [RNAseq quantification and NLP processing](https://docs.google.com/presentation/d/14vLJJQ6ziw-2aLDoQAJGyv1sYo5ENzljsqsbZr9jNLM/edit#slide=id.p19), explaining 1.) why the data is something that you can trust and 2.) also the utility of fast data interpolation, which is especially useful for aggregating multiple studies/batches to support your hypothesis. 

## Why Skymap while there are so many groups out there also trying to unify the public data
To the best of my knowledge, Skymap is the first that offer both the unified omic data and the cleaned metadata. The other important aspect is that the process of data extraction is fully automated, so it is supposed to be scalable and systematic. 

## Why Skymap offer a local copy instead of a web api 
Again, the purpose of this project is more geared towards bioinformatics/ data scientists, who wants go from vast amount of data to hypothesis quickly. I hate when I have to recover a simple table by requesting each row from REST api repeately, which should have only required one click on an ftp link. It turns out that even [all the raw meta data from SRA can fit into memory](https://github.com/brianyiktaktsui/Skymap/blob/master/Load_RawMetaData.ipynb). 

The premise of skymap is this: Couple clicks and all the omic data sits in your computer. And you can slice and dice it however you want afterwards. 

## Data format and coding style

The storage is in python pandas pickle format. Therefore, the only packges you need to load in the data is numpy and pandas, the backbone of data analysis in python. We keep the process of data loading as lean as possible. Less code means less bugs and less errors. For now, Skymap is geared towards ML/data science folks who are hungry for the vast amount of data and ain���t afraid of coding. I will port the data to native HDF5 format to reduce platform dependency once I get a chance. 

I tried to keep the code and parameters to be lean and self-explanatory for your reference. 


# Data slicing example

### Accessing allelic read count dataframe
Slice out >100k experiments and their allelic counts in < 1s


```python
### parameters
import pandas as pd
import numpy as np
mySpecie='Homo_sapiens'
#change base dir to your data location
baseDir='/cellar/users/btsui/Data/SRA/snp/'
skymap_snp_dir=baseDir+'{specie}_snp_pos/'.format(specie=mySpecie)
```

**input query BRAF V600 coordinate**


```python
#location where BRAF V600 happens, you can change it to whatever position you want 
queryChr,queryPosition='7',140753336 
```

**static code for slicing out the data**


```python
%%time
chunkSize=100000 #fixed params
myChunk=(queryPosition/chunkSize)*chunkSize # identify the chunk to load in
hdf_s=pd.HDFStore(skymap_snp_dir+'Pos_block_'+str(myChunk),mode='r')#load in the chunk
tmpChunkDf=hdf_s['/chunk'] 
```

    CPU times: user 112 ms, sys: 132 ms, total: 244 ms
    Wall time: 303 ms



```python
print '# of sequencing runs sliced out:' ,tmpChunkDf.Run_digits.nunique()
```

    # of sequencing runs sliced out: 149064


** definition of each column in allelic counts data**

Chr: Chromosome

Base: DNA bases in aligned reads - A, C, G, T 

Run_db and Run_digits together forms a SRR accession id. I ignored the leading 0s for Run_digits. 

ReadDepth: the number of bases detected in aligned reads at a particular base and chromosome position. 

AverageBaseQuality: The mean phred score in aligned reads at a particular base and chromosome postiion. 

Pos: Chromosome position. (grch38 for human)

block: the block ID used for chunked storage


```python
tmpChunkDf.head()
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th></th>
      <th>features</th>
      <th>Run_digits</th>
      <th>Pos</th>
      <th>ReadDepth</th>
      <th>AverageBaseQuality</th>
      <th>block</th>
    </tr>
    <tr>
      <th>Chr</th>
      <th>base</th>
      <th>Run_db</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th rowspan="5" valign="top">2</th>
      <th>C</th>
      <th>SRR</th>
      <td>796215</td>
      <td>140700401</td>
      <td>1</td>
      <td>41</td>
      <td>140700000</td>
    </tr>
    <tr>
      <th>A</th>
      <th>SRR</th>
      <td>5882370</td>
      <td>140700401</td>
      <td>1</td>
      <td>11</td>
      <td>140700000</td>
    </tr>
    <tr>
      <th rowspan="3" valign="top">C</th>
      <th>SRR</th>
      <td>3420530</td>
      <td>140700401</td>
      <td>140</td>
      <td>36</td>
      <td>140700000</td>
    </tr>
    <tr>
      <th>SRR</th>
      <td>586184</td>
      <td>140700401</td>
      <td>2</td>
      <td>35</td>
      <td>140700000</td>
    </tr>
    <tr>
      <th>SRR</th>
      <td>4444531</td>
      <td>140700401</td>
      <td>16</td>
      <td>39</td>
      <td>140700000</td>
    </tr>
  </tbody>
</table>
</div>



### Accessing RNAseq dataframe

Read out any gene expression level for >100k of experiments in 10ms. 

input: genename, output: experiment by TPM vector


```python
"""
a standalone function for memory mapping the data
"""
def loadDf(fname,mmap_mode='r'):
    with open(fname+'.index.txt') as f:
        myIndex=map(lambda s:s.replace("\n",""), f.readlines())
    with open(fname+'.columns.txt') as f:
        myColumns=map(lambda s:s.replace("\n",""), f.readlines())
    tmpMatrix=np.load(fname+".npy",mmap_mode=mmap_mode)
    tmpDf=pd.DataFrame(tmpMatrix,index=myIndex,columns=myColumns)
    tmpDf.columns.name='Run'
    return tmpDf
```


```python
expressionMetric='TPM'
#change this to where the matrix is located on your computer
baseDir='/cellar/users/btsui/Data/nrnb01_nobackup/Data/SRA/MATRIX/DATA/hgGRC38/'
dataMatrixDir=baseDir+'/allSRAmatrix.realign.v9.base.{feature}.gene.symbol'.format(feature=expressionMetric)
```


```python
%%time
rnaseqDf=loadDf(dataMatrixDir)
```

    CPU times: user 120 ms, sys: 24 ms, total: 144 ms
    Wall time: 134 ms



```python
%%time
geneS=rnaseqDf.loc['CDK1']
```

    CPU times: user 4 ms, sys: 0 ns, total: 4 ms
    Wall time: 7.39 ms



```python
geneS.head()
```




    Run
    SRR4456480    56.119999
    SRR4456481     0.000000
    SRR4456482     0.000000
    SRR4456483     0.000000
    SRR4456484     0.000000
    Name: CDK1, dtype: float32



### Accesing biological metadata dataframe

For more information about bio_metaDf columns:

Sample: https://www.ncbi.nlm.nih.gov/books/NBK56913/

attribute: https://www.ncbi.nlm.nih.gov/biosample/docs/attributes/

NCIT_Eng, NCIT_ID: https://ncit.nci.nih.gov/

NLM_CUI: https://www.nlm.nih.gov/research/umls/new_users/online_learning/Meta_005.html

The NLP tool used for mapping freetexts to terms is called metamap:
https://metamap.nlm.nih.gov/


```python
metaDataMappingSDir='/cellar/users/btsui/Data/nrnb01_nobackup/METAMAP//input/allAttrib.v5.csv.NCI.prefilter.pyc'
bio_metaDf=pd.read_pickle(metaDataMappingSDir)
```

Here is how it looks like


```python
bio_metaDf.head()
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>srs</th>
      <th>attrib</th>
      <th>CUI</th>
      <th>score</th>
      <th>NCI</th>
      <th>NciEng</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>SRS286232</td>
      <td>sex</td>
      <td>C1706180</td>
      <td>1000</td>
      <td>C46109</td>
      <td>Male Gender</td>
    </tr>
    <tr>
      <th>1</th>
      <td>SRS286232</td>
      <td>sex</td>
      <td>C1706429</td>
      <td>1000</td>
      <td>C46107</td>
      <td>Male, Self-Report</td>
    </tr>
    <tr>
      <th>2</th>
      <td>SRS286232</td>
      <td>sex</td>
      <td>C1706428</td>
      <td>1000</td>
      <td>C46112</td>
      <td>Male Phenotype</td>
    </tr>
    <tr>
      <th>3</th>
      <td>DRS052357</td>
      <td>BioSampleModel</td>
      <td>C1332821</td>
      <td>694</td>
      <td>C24597</td>
      <td>CXCL9 Gene</td>
    </tr>
    <tr>
      <th>4</th>
      <td>DRS052357</td>
      <td>BioSampleModel</td>
      <td>C1707170</td>
      <td>694</td>
      <td>C49770</td>
      <td>CXCL9 wt Allele</td>
    </tr>
  </tbody>
</table>
</div>




```python
print '# of unique biological sample annotations with terms extracted:',bio_metaDf['srs'].nunique()
```

    # of unique biological sample annotations with terms extracted: 3068221


Millions of biological annotations have NLP key words extracted with high number of unique terms, suggesting that public data deposited in SRA has both high volumne and diversity in experimental conditions. 


```python
print '# of unique biomedical terms:',bio_metaDf['NCI'].nunique()
```

    # of unique biomedical terms: 20150


### Accessing technical metadata dataframe

For more information about the aliases used in the follow meta data:

https://www.ncbi.nlm.nih.gov/books/NBK56913/




```python
##change the directory
sra_dump_pickle_dir='/cellar/users/btsui/Data/SRA/DUMP/sra_dump.pickle'
technical_meta_data_df=pd.read_pickle(sra_dump_pickle_dir)
```


```python
print '# of SRRs: ',technical_meta_data_df.shape[0]
```

    # of SRRs:  3763299



```python
technical_meta_data_df.head()
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Member_Name</th>
      <th>Experiment</th>
      <th>Sample</th>
      <th>Study</th>
      <th>Spots</th>
      <th>Bases</th>
      <th>Status</th>
      <th>ScientificName</th>
      <th>LibraryStrategy</th>
      <th>LibraryLayout</th>
      <th>...</th>
      <th>proj_accession_Updated</th>
      <th>proj_accession_Published</th>
      <th>proj_accession_Received</th>
      <th>proj_accession_Type</th>
      <th>proj_accession_Center</th>
      <th>proj_accession_Visibility</th>
      <th>proj_accession_Loaded</th>
      <th>proj_accession_ReplacedBy</th>
      <th>Run_db</th>
      <th>Run_digits</th>
    </tr>
    <tr>
      <th>Run</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>SRR2401865</th>
      <td>default</td>
      <td>SRX1244330</td>
      <td>SRS1068422</td>
      <td>-</td>
      <td>2800.0</td>
      <td>1416405.0</td>
      <td>live</td>
      <td>soil_metagenome</td>
      <td>AMPLICON</td>
      <td>SINGLE</td>
      <td>...</td>
      <td>2015-09-22</td>
      <td>2015-09-20</td>
      <td>2015-09-15</td>
      <td>RUN</td>
      <td>SUB1095135</td>
      <td>public</td>
      <td>1</td>
      <td>-</td>
      <td>SRR</td>
      <td>2401865</td>
    </tr>
    <tr>
      <th>SRR2401866</th>
      <td>default</td>
      <td>SRX1244331</td>
      <td>SRS1068421</td>
      <td>-</td>
      <td>5082.0</td>
      <td>2563605.0</td>
      <td>live</td>
      <td>soil_metagenome</td>
      <td>AMPLICON</td>
      <td>SINGLE</td>
      <td>...</td>
      <td>2015-09-22</td>
      <td>2015-09-20</td>
      <td>2015-09-15</td>
      <td>RUN</td>
      <td>SUB1095135</td>
      <td>public</td>
      <td>1</td>
      <td>-</td>
      <td>SRR</td>
      <td>2401866</td>
    </tr>
    <tr>
      <th>SRR2401867</th>
      <td>default</td>
      <td>SRX1244332</td>
      <td>SRS1068420</td>
      <td>-</td>
      <td>6169.0</td>
      <td>3175528.0</td>
      <td>live</td>
      <td>soil_metagenome</td>
      <td>AMPLICON</td>
      <td>SINGLE</td>
      <td>...</td>
      <td>2015-09-22</td>
      <td>2015-09-20</td>
      <td>2015-09-15</td>
      <td>RUN</td>
      <td>SUB1095135</td>
      <td>public</td>
      <td>1</td>
      <td>-</td>
      <td>SRR</td>
      <td>2401867</td>
    </tr>
    <tr>
      <th>SRR2401868</th>
      <td>default</td>
      <td>SRX1244333</td>
      <td>SRS1068419</td>
      <td>-</td>
      <td>8102.0</td>
      <td>4266915.0</td>
      <td>live</td>
      <td>soil_metagenome</td>
      <td>AMPLICON</td>
      <td>SINGLE</td>
      <td>...</td>
      <td>2015-09-22</td>
      <td>2015-09-20</td>
      <td>2015-09-15</td>
      <td>RUN</td>
      <td>SUB1095135</td>
      <td>public</td>
      <td>1</td>
      <td>-</td>
      <td>SRR</td>
      <td>2401868</td>
    </tr>
    <tr>
      <th>SRR2401869</th>
      <td>default</td>
      <td>SRX1244334</td>
      <td>SRS1068418</td>
      <td>-</td>
      <td>4971.0</td>
      <td>2519200.0</td>
      <td>live</td>
      <td>soil_metagenome</td>
      <td>AMPLICON</td>
      <td>SINGLE</td>
      <td>...</td>
      <td>2015-09-22</td>
      <td>2015-09-20</td>
      <td>2015-09-15</td>
      <td>RUN</td>
      <td>SUB1095135</td>
      <td>public</td>
      <td>1</td>
      <td>-</td>
      <td>SRR</td>
      <td>2401869</td>
    </tr>
  </tbody>
</table>
<p>5 rows �� 22 columns</p>
</div>



# More examples on using simple code to analyze big data

**If you intend to run the example notebooks, first download the data from synapse**

https://www.synapse.org/#!Synapse:syn11415602/wiki/492470


## High resolution mouse developmental hierachy map
[Link](https://github.com/brianyiktaktsui/Skymap/blob/master/jupyter-notebooks/clean_notebooks/TemporalQuery_V4_all_clean.ipynb
)

Aggregating many studies (node) to form a smooth mouse developmental hierachy map. By integrating the vast amount of public data, we can cover many developmental time points, which sometime we can see a more transient expression dynamics both across tissues and within tissues over developmental time course. 

Each componenet represent a tissue. Each node represent a particular study at a particular time unit. The color is base on the developmental time extracted from experimental annotation using regex. The node size represent the # of sequencing runs in that particulr time point and study. Each edge represent a differentiate-to or part-of relationship.
![alt text](./Figures/heirachy_time.png "Logo Title Text 1")
And you can easily overlay gene expression level on top of it. As an example, Tp53 expression is known to be tightly regulated in development. Let's look at the dynamic of Tp53 expression over time and spatial locations in the following plot.
![alt_text](./Figures/heirachy_Trp53.png "tp53")

## Locating  SNP and correlating with different data layers
https://github.com/brianyiktaktsui/Skymap/blob/master/FindStudiesWithBrafV600Mutated.ipynb
## Simple RNAseq data slicing and hypothesis testing
https://github.com/brianyiktaktsui/Skymap/blob/master/DataSlicingExample.ipynb

[Check here for more example notebooks](https://github.com/brianyiktaktsui/Skymap/tree/master/jupyter-notebooks
)

The code for the pipelines is here:
https://github.com/brianyiktaktsui/Skymap/tree/master/code

Skymap is still in Beta V0.0. [Please feel free to leave comments](https://www.synapse.org/#!Synapse:syn11415602/discussion/default) and suggestions!!! We would love to hear feedbacks from you.
## Acknowledgement


Please considering citing if you are using Skymap. (doi:10.7303/syn11415602)

Acknowledgement: We want to thank for the advice and resources from Dr. Hannah Carter (my PI), Dr. Jill Mesirov,Dr. Trey Ideker and Shamin Mollah. We also want to thank Dr. Ruben Arbagayen, Dr. Nate Lewis for their suggestion. 
The method will soon be posted in bioarchive. Also, we want to thank the Sage Bio Network for hosting the data. We also thank to thank the NCBI for holding all the published raw reads at  [Sequnece Read Archive](https://www.ncbi.nlm.nih.gov/sra). 
Grant money that make this work possible: NIH DP5OD017937,GM103504

Term of use: Use Skymap however you want. Just dont sue me, I have no money. 

For why I named it Skymap, I forgot.



```python
!jupyter nbconvert --to markdown README.ipynb
!git add README.md
!git commit -m "updated: README"
!git push 
```


```python
#!cp -r ./Skymap_legacy-master/Figures/ ./Figures
```

# TO UPDATE SRA META DATA


|Steps | Code| Input description|Input dir|Output description|Output dir| Timing|
|---- | ----| ----|----|----|----| ----|
|download SRA metadata | ./Pipelines/Update_SRA_meta_data/pull_SRA_meta.ipynb|none, download from web||SRA meta data| /nrnb/users/btsui/tmp/SRA_META/| 30 mins|
|parse SRA metadata | ./SRA_META/SRAManager.py |  SRA files in XML formats|/nrnb/users/btsui/tmp/SRA_META/| list of pandas series containing list of (SRS,attribute, freetext) | /cellar/users/btsui/Data/nrnb01_nobackup/tmp/METAMAP//splittedInput_SRAMangaer_SRA_META/| 20 mins
|merge SRA metadata | ./SRA_META/SRAmerge.py | list of pandas series containing list of (SRS,attribute, freetext) |/cellar/users/btsui/Data/nrnb01_nobackup/tmp/METAMAP//splittedInput_SRAMangaer_SRA_META/(allSRS.pickle,allSRX.pickle) |all SRA SRS biospecieman annotation in allSRS.pickle and allSRX.pickle  | /cellar/users/btsui/Data/nrnb01_nobackup/METAMAP/ | 10 mins| 


|Steps | Code| Input description|Input dir|Output description|Output dir| Timing|
|---- | ----| ----|----|----|----| ----|
|calculate the SNP for extraction | ./Pipelines/snp/calculate_unprocessed.py


```python
#!cat ./Pipelines/snp/single_snp.py
```


```python
#!samtools --version
```


```python
#!/cellar/users/btsui/Program/bam_read_count/bam-readcount-master/bin/bam-readcount --version
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



```python
!jupyter nbconvert --to markdown README.ipynb
!git add README.md
!git commit -m "updated: README"
!git push 
```

    [NbConvertApp] Converting notebook README.ipynb to markdown
    [NbConvertApp] Writing 5841 bytes to README.md
    [master 511e331] updated: README
     1 file changed, 5 insertions(+), 8 deletions(-)
    warning: push.default is unset; its implicit value has changed in
    Git 2.0 from 'matching' to 'simple'. To squelch this message
    and maintain the traditional behavior, use:
    
      git config --global push.default matching
    
    To squelch this message and adopt the new behavior now, use:
    
      git config --global push.default simple
    
    When push.default is set to 'matching', git will push local branches
    to the remote branches that already exist with the same name.
    
    Since Git 2.0, Git defaults to the more conservative 'simple'
    behavior, which only pushes the current branch to the corresponding
    remote branch that 'git pull' uses to update the current branch.
    
    See 'git help config' and search for 'push.default' for further information.
    (the 'simple' mode was introduced in Git 1.7.11. Use the similar mode
    'current' instead of 'simple' if you sometimes use older versions of Git)
    
    Counting objects: 3, done.
    Delta compression using up to 96 threads.
    Compressing objects: 100% (2/2), done.
    Writing objects: 100% (3/3), 355 bytes | 0 bytes/s, done.
    Total 3 (delta 1), reused 0 (delta 0)
    remote: Resolving deltas: 100% (1/1), completed with 1 local object.[K
    To git@github.com:brianyiktaktsui/AllPipes.git
       b063c6e..511e331  master -> master



```python
#! gdc-client --version
```


```python
#!unzip Skymap_legacy-master.zip
```

    Archive:  Skymap_legacy-master.zip
    867d0776718e5c768d8268dcf811dd05c8196440
       creating: Skymap_legacy-master/
      inflating: Skymap_legacy-master/DataSlicingExample.ipynb  
       creating: Skymap_legacy-master/Figures/
     extracting: Skymap_legacy-master/Figures/README  
      inflating: Skymap_legacy-master/Figures/heirachy_Trp53.png  
      inflating: Skymap_legacy-master/Figures/heirachy_time.png  
      inflating: Skymap_legacy-master/Figures/sra_data_availability.png  
      inflating: Skymap_legacy-master/FindStudiesWithBrafV600Mutated.ipynb  
      inflating: Skymap_legacy-master/FindStudiesWithBrafV600Mutated_without_demo.md  
      inflating: Skymap_legacy-master/Load_RawMetaData.ipynb  
      inflating: Skymap_legacy-master/README.md  
       creating: Skymap_legacy-master/code/
       creating: Skymap_legacy-master/code/NLP/
      inflating: Skymap_legacy-master/code/NLP/MetamapParser.py  
      inflating: Skymap_legacy-master/code/NLP/NCITerminology.py  
      inflating: Skymap_legacy-master/code/NLP/NCITerminologyParam.py  
     extracting: Skymap_legacy-master/code/NLP/README  
      inflating: Skymap_legacy-master/code/NLP/SRAManager.py  
      inflating: Skymap_legacy-master/code/NLP/SRAParam.py  
      inflating: Skymap_legacy-master/code/NLP/SRAParser.py  
      inflating: Skymap_legacy-master/code/NLP/SRA_dump_refresh.py  
      inflating: Skymap_legacy-master/code/NLP/SRAmerge.py  
      inflating: Skymap_legacy-master/code/NLP/__init__.py  
      inflating: Skymap_legacy-master/code/NLP/clusterBaseClass.py  
      inflating: Skymap_legacy-master/code/NLP/clusterRun.py  
      inflating: Skymap_legacy-master/code/NLP/inputPartitionerText.py  
      inflating: Skymap_legacy-master/code/NLP/mergeKmeanResults.py  
      inflating: Skymap_legacy-master/code/NLP/metamapParam.py  
      inflating: Skymap_legacy-master/code/NLP/metamapParsingManager.py  
      inflating: Skymap_legacy-master/code/NLP/metamapping.py  
      inflating: Skymap_legacy-master/code/NLP/metamappingManager.py  
      inflating: Skymap_legacy-master/code/NLP/sharedFunctionGraph.py  
      inflating: Skymap_legacy-master/code/NLP/sharedFunctionParsing.py  
      inflating: Skymap_legacy-master/code/NLP/sharedVariable.py  
       creating: Skymap_legacy-master/code/pipelines/
       creating: Skymap_legacy-master/code/pipelines/snp/
     extracting: Skymap_legacy-master/code/pipelines/snp/README  
      inflating: Skymap_legacy-master/code/pipelines/snp/calculate_unprocessed.py  
      inflating: Skymap_legacy-master/code/pipelines/snp/decouple_fastq.py  
      inflating: Skymap_legacy-master/code/pipelines/snp/paired_snp.py  
      inflating: Skymap_legacy-master/code/pipelines/snp/param.py  
      inflating: Skymap_legacy-master/code/pipelines/snp/param.pyc  
      inflating: Skymap_legacy-master/code/pipelines/snp/run_one.py  
      inflating: Skymap_legacy-master/code/pipelines/snp/single_snp.py  
      inflating: Skymap_legacy-master/code/pipelines/snp/snp_all_seq.sh  
       creating: Skymap_legacy-master/jupyter-notebooks/
       creating: Skymap_legacy-master/jupyter-notebooks/clean_notebooks/
      inflating: Skymap_legacy-master/jupyter-notebooks/clean_notebooks/AllSeqBySpecies.ipynb  
      inflating: Skymap_legacy-master/jupyter-notebooks/clean_notebooks/CompareTCGA_alignment_w_mine_pipe.ipynb  
     extracting: Skymap_legacy-master/jupyter-notebooks/clean_notebooks/README  
      inflating: Skymap_legacy-master/jupyter-notebooks/clean_notebooks/TemporalQuery_V4_all_clean.ipynb  
     extracting: Skymap_legacy-master/jupyter-notebooks/readme  

