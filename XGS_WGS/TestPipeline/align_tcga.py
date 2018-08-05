import pandas as pd
import sys
import os
import time

#i=0
i=int(sys.argv[1])-1

manifest_dir='/cellar/users/btsui/Project/METAMAP/notebook/RapMapTest/XGS_WGS/tcga_lgg_wgs_bams.df.wxs_rnaseq.pickle'
token_dir='/cellar/users/ramarty/tokens/gdc-user-token.2018-06-25T22_21_40.089Z.txt'
bam_read_count_dir='/cellar/users/btsui/Program/bam_read_count/bam-readcount-master/bin/bam-readcount'

gdc_cmd_fmt='gdc-client download -t {token_dir} -d {out_dir} {file_uuid}'
out_dir='/nrnb/users/btsui/Data/tcga_raw_lgg/'

manifest_df=pd.read_pickle(manifest_dir)
manifest_S=manifest_df.iloc[i]

file_uuid=manifest_S['file_id']
print ('UUID: ',file_uuid)

gdc_cmd=gdc_cmd_fmt.format(out_dir=out_dir,file_uuid=file_uuid,token_dir=token_dir)

result = os.system(gdc_cmd)
### pipe the data
tmpDir=out_dir+file_uuid+'/'
os.chdir(tmpDir)

os.system('rm fastq_pipe')

os.system('mkfifo fastq_pipe')
os.system('bamToFastq -i {} -fq fastq_pipe &'.format(manifest_S['file_name']))

### align using bowtie2


#os.system('align using bowtie2 ')
#/cellar/users/btsui/Data/BOWTIE2_GENOME_INDEX/
#/cellar/users/btsui/Data/BOWTIE_GENOME_SNP_INDEX/
#other bases 
baseGenomesDir='/cellar/users/btsui/Data/BOWTIE2_GENOME_INDEX/'
specie='Homo_sapiens'
genomeDir=baseGenomesDir+'/'+specie+'/bowtie2'
cmd_algn='bowtie2 --local -x {ref} -U fastq_pipe --no-unal --threads 8 | samtools view -bS - -o unalgn.bam '.format(ref=genomeDir)

###align
t0 = time.time()
os.system(cmd_algn)
t1 = time.time()
total = t1-t0
print ('time for alignment:'+str(total))

####sort
t0 = time.time()
os.system('samtools sort unalgn.bam -o sorted.bam')
t1 = time.time()
total = t1-t0
print ('time for sorting:'+str(total))

print ('\n')
os.system('ls -lath')
os.system('rm -r '+tmpDir)
#!ls -lath

"""
cmd_algn='bowtie2 --local -x {ref} -U fastq_pipe --no-unal --threads 8 | samtools view -bS - | samtools sort -  sorted.bam  2>bowtie_log.txt'.format(ref=genomeDir)
"""
