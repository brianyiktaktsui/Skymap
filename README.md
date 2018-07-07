
# In short
Skymap is a standalone database that offers: 
1. **a single data matrix** for each omic layer for each species that [spans >200k sequencing runs from all the public studies](https://www.ncbi.nlm.nih.gov/sra), which is done by reprocessing **petabytes** worth of sequencing data. Here is how much published data are deposited in SRA: 
![alt text](./Figures/sra_data_availability.png "Logo Title Text 1")**And here is how much data we have processed from SRA:**
![alt text](./Figures/sra_data_processed.png)
2. **a biological metadata file** that describe the relationships between the sequencing runs and also the keywords extracted from over **3 million** freetext annotations using NLP. 
3. **a techinical metadata file** that describe the relationships between the sequencing runs. 


**Where they can all fit into your personal computer.**

**If you intend to run the examples, please first download the data from here:** 
* https://www.synapse.org/skymap (take < 3 minutes to set up the account). 


# More examples on using simple code to analyze big data


## High resolution mouse developmental hierachy map
[jupyter notebook link](https://github.com/brianyiktaktsui/Skymap/blob/master/jupyter-notebooks/clean_notebooks/TemporalQuery_V4_all_clean.ipynb
)

Aggregating many studies (node) to form a smooth mouse developmental hierachy map. By integrating the vast amount of public data, we can cover many developmental time points, which sometime we can see a more transient expression dynamics both across tissues and within tissues over developmental time course. 

Each componenet represent a tissue. Each node represent a particular study at a particular time unit. The color is base on the developmental time extracted from experimental annotation using regex. The node size represent the # of sequencing runs in that particulr time point and study. Each edge represent a differentiate-to or part-of relationship.
![alt text](./Figures/heirachy_time.png "Logo Title Text 1")
And you can easily overlay gene expression level on top of it. As an example, Tp53 expression is known to be tightly regulated in development. Let's look at the dynamic of Tp53 expression over time and spatial locations in the following plot.
![alt_text](./Figures/heirachy_Trp53.png "tp53")

## Locating  SNP and correlating with different data layers
[jupyter notebook link](https://github.com/brianyiktaktsui/Skymap/blob/master/FindStudiesWithBrafV600Mutated.ipynb)
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

## Data format and coding style

The storage is in python pandas pickle format. Therefore, the only packges you need to load in the data is numpy and pandas, the backbone of data analysis in python. We keep the process of data loading as lean as possible. Less code means less bugs and less errors. For now, Skymap is geared towards ML/data science folks who are hungry for the vast amount of data and ain't afraid of coding. I will port the data to native HDF5 format to reduce platform dependency once I get a chance. 

I tried to keep the code and parameters to be lean and self-explanatory for your reference. 



## Methods
If you want to better understand the NLP platform, I have another github page for the NLP explanation: 
* [Deep biomedical named  NLP engine](https://github.com/brianyiktaktsui/DEEP_NLP)

If you want to understand meta-analyisis using RNAseq and extracted metadata, I have written an manuscript that kinda explain that: 
* [legacy Skymap for RNAseq and using Metamap as NLP engine](https://docs.google.com/document/d/1_nES7vroX7lCwf5NSNBVZ1k2iubYm5wLeFqusq5aZuk) 


# update pipeline

If you happen to want to make a copy of the pipeline, you probably want to be be more careful about it. 

### TO UPDATE SRA META DATA


|Steps | Code| Input description|Input dir|Output description|Output dir| Timing|
|---- | ----| ----|----|----|----| ----|
|download SRA metadata | ./Pipelines/Update_SRA_meta_data/pull_SRA_meta.ipynb|none, download from web||SRA meta data| /nrnb/users/btsui/tmp/SRA_META/| 30 mins|
|parse SRA metadata | ./SRA_META/SRAManager.py |  SRA files in XML formats|/nrnb/users/btsui/tmp/SRA_META/| list of pandas series containing list of (SRS,attribute, freetext) | /cellar/users/btsui/Data/nrnb01_nobackup/tmp/METAMAP//splittedInput_SRAMangaer_SRA_META/| 20 mins
|merge SRA metadata | ./SRA_META/SRAmerge.py | list of pandas series containing list of (SRS,attribute, freetext) |/cellar/users/btsui/Data/nrnb01_nobackup/tmp/METAMAP//splittedInput_SRAMangaer_SRA_META/(allSRS.pickle,allSRX.pickle) |all SRA SRS biospecieman annotation in allSRS.pickle and allSRX.pickle  | /cellar/users/btsui/Data/nrnb01_nobackup/METAMAP/ | 10 mins| 


### To update the SNP pipeline: 

The way I organized the code is trying to keep the code as simple as possible. 
For each pipeline, it has 6 scripts, <500 lines each to ensure readability. Run each pipeliine starting with calcuate_uprocessed.py, which calculate the number of files still require for processing.


|Pipeline | Code| Input description|Input dir|Output description|Output dir| Timing|
|---- | ----| ----|----|----|----| ----|
|SNP extraction | ./Pipelines/snp/calculate_unprocessed.py|
|calculating reads coverage | ./Pipelines/chip/calculate_unprocessed.py|
|RNAseq| ./Pipelines/RNAseq/calculate_unprocessed.py |


```python
#!ls ./SRA_META/
```


```python
!wc -l ./Pipelines/snp/*.py
```

       30 ./Pipelines/snp/calculate_unprocessed.py
       12 ./Pipelines/snp/decouple_fastq.py
      135 ./Pipelines/snp/old_single_end_tcga.py
      152 ./Pipelines/snp/paired_snp.py
        9 ./Pipelines/snp/param.py
       17 ./Pipelines/snp/run_one.py
      137 ./Pipelines/snp/single_snp.py
      492 total



```python
!cat ./Pipelines/snp/paired_snp.py
```

    #run at '/cellar/users/btsui/Project/METAMAP/notebook/RapMapTest/Pipelines/'
    import os,sys
    sys.path+=['/cellar/users/btsui/Project/METAMAP/notebook/RapMapTest/Pipelines/snp/']
    import pandas as pd
    import subprocess
    from multiprocessing import Process
    import param
    TEST=False
    nThread=3
    def startChildren(cmd):
        def f():
            os.system(cmd) 
        p = Process(target=f)
        p.start()
        return p
    specieToRefDict={'Homo_sapiens':'Homo_sapiens.GRCh38.dna_rm.toplevel.fa'}
    
    if TEST:
        srrRun='ERR1569091'
        specie='Homo_sapiens'
    else:
        srrRun=sys.argv[1]
        specie=sys.argv[2]
        
    print srrRun,specie
    baseGenomesDir='/cellar/users/btsui/Data/BOWTIE_GENOME_SNP_INDEX/'
    #out_dir='
    base_dict_dir='/cellar/users/btsui/Data/Project/Skymap/ChipSeq/empty_references/'
    log_out_dir=param.log_out_dir#'/cellar/users/btsui/Data/SRA/all_seq/log/'
    count_out_dir=param.count_out_dir#'/cellar/users/btsui/Data/SRA/all_seq/chip/'
    genomeDir=baseGenomesDir+specie+'/bowtie2'
    tmp_dir="/tmp/SRA_DATA/"
    
    #count_script_dir='/cellar/users/btsui/Project/METAMAP/notebook/RapMapTest/Chip-seq/a.out'
    SRA_FASTQ_TOOL_DIR="/cellar/users/btsui/Program/SRA_TOOL_KIT/sratoolkit.2.4.2-ubuntu64/bin/fastq-dump.2.4.2"
    myoption=r'"/cellar/users/btsui/.aspera/connect/bin/ascp|/cellar/users/btsui/.aspera/connect/etc/asperaweb_id_dsa.openssh"'
    trim_galore_Dir='/cellar/users/btsui/Program/TRIMAGLORE//trim_galore'
    bam_read_count_dir='/cellar/users/btsui/Program/bam_read_count/bam-readcount-master/bin/bam-readcount'
    snpBed='/cellar/users/btsui/Data/dbsnp/snp_beds/'+specie+'.bed'
    fa_dir='/cellar/users/btsui/Data/ensembl/release/fasta/'+specieToRefDict[specie]
    
    base_sra_dir='/tmp/btsui/METH/sra/'
    
    ##make temperoary directory
    job_tmp_dir=tmp_dir+srrRun+"/"
    subprocess.call(["rm", "-rf",job_tmp_dir])#remove the directory before running STAR
    subprocess.call(["mkdir", "-p",job_tmp_dir]) #tmp dir for processing
    os.chdir(job_tmp_dir)
    ##download sra file
    #downloadCommand=['prefetch','-t','ascp','--ascp-path',myoption,' --ascp-options "-l 2000000" ',srrRun]
    downloadCommand=['prefetch',srrRun]
    os.system(' '.join(downloadCommand))
    
    ##identify adaptor contents using first 10000 reads
    #--paired
    myCmd='{sra_dump_dir} --split-files --stdout {sra_file_dir} |head -n 16000 > head.fq'.format(sra_dump_dir=SRA_FASTQ_TOOL_DIR,                                    sra_file_dir=base_sra_dir+srrRun+'.sra',trim_galore_Dir=trim_galore_Dir)
    os.system(myCmd) 
    os.system('/cellar/users/btsui/Project/METAMAP/notebook/RapMapTest/Pipelines/snp/decouple_fastq.py'+' head.fq')
    
    os.system(trim_galore_Dir+' --paired '+' head.fq_R1 head.fq_R2')
    ##identify adaptor contents
    fq_trimming_report_S=pd.Series.from_csv('head.fq_R1_trimming_report.txt',index_col=None,sep='\t\t\t\t\\t\t\tt')
    adapter_sequence_1=fq_trimming_report_S.str.extract("Adapter sequence: '(\w+)'",expand=False).dropna().iloc[0]
    
    
    fq_trimming_report_S=pd.Series.from_csv('head.fq_R2_trimming_report.txt',index_col=None,sep='\t\t\t\t\\t\t\tt')
    adapter_sequence_2=fq_trimming_report_S.str.extract("Adapter sequence: '(\w+)'",expand=False).dropna().iloc[0]
    
    ##set up pipe for counting the data
    ##remove pipes if they exist 
    os.system('rm {srrRun}_bowtie {srrRun}_count '.format(srrRun=srrRun))
    os.system('mkfifo {srrRun}_bowtie {srrRun}_count '.format(srrRun=srrRun))
    
    #my_dict_dir=base_dict_dir+specie+'.size.tsv'
    #cmd_0='{count_script_dir} {my_dict_dir} {srrRun}_count'.format(
    #    count_script_dir=count_script_dir,srrRun=srrRun,my_dict_dir=my_dict_dir)
    if TEST:#in test case, for min read length
        cmd_4="genomeCoverageBed -pc -ibam file_sorted -bg| awk '{ if ($4 >= 1) { print } }' >out.bg"
    else:
        cmd_4="genomeCoverageBed -pc -ibam file_sorted -bg| awk '{ if ($4 >= 5) { print } }' >out.bg"
        
    cmd_0='samtools view -bS {srrRun}_count | samtools sort - > file_sorted'.format(srrRun=srrRun)
    
    #bowtie that support interleave
    bowtie2_dir='/cellar/users/btsui/Program/bowtie2-2.3.4-linux-x86_64/bowtie2'
    
    cmd_1='{bowtie2_dir}  -x {ref} --interleaved {srrRun}_bowtie --threads {nThread} > {srrRun}_count 2>bowtie_log.txt'.format(ref=genomeDir,srrRun=srrRun,nThread=nThread,bowtie2_dir=bowtie2_dir)
    #take in and sort it 
    
    if TEST:
        cmd_2_fmt='{sra_dump_dir} --stdout --split-files {sra_file_dir} | head -n 8000 |cutadapt --interleaved -a {adapter_sequence_1} -A {adapter_sequence_2} - > {srrRun}_bowtie'
    else:
        cmd_2_fmt='{sra_dump_dir} --stdout --split-files {sra_file_dir} |cutadapt --interleaved -a {adapter_sequence_1} -A {adapter_sequence_2} - > {srrRun}_bowtie'
        
    cmd_2=cmd_2_fmt.format(
     sra_file_dir=base_sra_dir+srrRun+'.sra',srrRun=srrRun,adapter_sequence_1=adapter_sequence_1,adapter_sequence_2=adapter_sequence_2,sra_dump_dir=SRA_FASTQ_TOOL_DIR)
    
    ##### code specific to my data 
    ###execute code
    
    my_p_l=[startChildren(cmd_1), startChildren(cmd_2)]
    
    os.system(cmd_0)
    
    ###index and identify the regions of interest
    os.system('samtools index file_sorted')
    os.system('samtools idxstats file_sorted |gzip> per_fa_record_stat.txt.gz')##ADDED
    
    
    cmd_5=bam_read_count_dir+' -l '+snpBed+' -f '+fa_dir+' file_sorted |gzip > snp.txt.gz'
    os.system(cmd_5)
    
    os.system('echo ">>>>bowtie2 log" >log.txt')
    os.system('tail -n 10 bowtie_log.txt >>log.txt')
    os.system('echo ">>>>head.fq_trimming_report.txt">>log.txt')
    os.system('cat ./head.fq_R*_trimming_report.txt >> log.txt')
    ###
    os.system('cp log.txt {log_out_dir}/{srrRun}.log'.format(log_out_dir=log_out_dir,
                                                            srrRun=srrRun))
    os.system('cp snp.txt.gz {count_out_dir}/{srrRun}.txt.snp.gz'.format(
        count_out_dir=count_out_dir,srrRun=srrRun))
    os.system('cp per_fa_record_stat.txt.gz {count_out_dir}/{srrRun}_per_fa_record_stat.txt.gz'.format(
        count_out_dir=count_out_dir,srrRun=srrRun))##ADDED
    os.system('rm -r '+job_tmp_dir)
    os.system('rm '+base_sra_dir+srrRun+'.sra')
    os._exit(0)
    
    
    """
    print cmd_0
    print cmd_1
    print cmd_2
    my_p_l=[startChildren(cmd_0),startChildren(cmd_1),startChildren(cmd_2)]
    os.system(cmd_4)
    #os.system('gzip out.bg')
    tmp_cmd='gzip -c out.bg >  {count_out_dir}/{srrRun}.bg.gz'.format(count_out_dir=count_out_dir,srrRun=srrRun)
    os.system(tmp_cmd)
    
    os.system('echo ">>>>bowtie2 log" >log.txt')
    os.system('tail -n 10 bowtie_log.txt >>log.txt')
    os.system('echo ">>>>head.fq_trimming_report.txt">>log.txt')
    os.system('cat head.fq_R1_trimming_report.txt >> log.txt')
    os.system('cat head.fq_R2_trimming_report.txt >> log.txt')
    
    os.system('cp log.txt {log_out_dir}/{srrRun}.log'.format(log_out_dir=log_out_dir,
                                                            srrRun=srrRun))
    
    
    os.system('rm -r '+job_tmp_dir)
    os.system('rm '+base_sra_dir+srrRun+'.sra')
    os._exit(0)
    """



```python
!jupyter nbconvert --to markdown README.ipynb
!git add README.md ./jupyter-notebooks/clean_notebooks/*
!git commit -m "updated: README"
!git push 
```

    [NbConvertApp] Converting notebook README.ipynb to markdown
    [NbConvertApp] Writing 9763 bytes to README.md
    [master 16ed0f6] updated: README
     1 file changed, 8 insertions(+), 8 deletions(-)
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
    Compressing objects: 100% (3/3), done.
    Writing objects: 100% (3/3), 570 bytes | 0 bytes/s, done.
    Total 3 (delta 1), reused 0 (delta 0)
    remote: Resolving deltas: 100% (1/1), completed with 1 local object.[K
    remote: This repository moved. Please use the new location:[K
    remote:   git@github.com:brianyiktaktsui/Skymap.git[K
    To git@github.com:brianyiktaktsui/AllPipes.git
       4a03595..16ed0f6  master -> master



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

