
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

The storage is in python pandas pickle format. Therefore, the only packges you need to load in the data is numpy and pandas, the backbone of data analysis in python. We keep the process of data loading as lean as possible. Less code means less bugs and less errors. For now, Skymap is geared towards ML/data science folks who are hungry for the vast amount of data and ain't afraid of coding. I will port the data to native HDF5 format to reduce platform dependency once I get a chance. 

I tried to keep the code and parameters to be lean and self-explanatory for your reference. 




```python
!jupyter nbconvert --to markdown README.ipynb
!git add README.md #./Figures/*
!git commit -m "updated: README"
!git push 
```

    [NbConvertApp] Converting notebook README.ipynb to markdown
    [NbConvertApp] Writing 15428 bytes to README.md



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
