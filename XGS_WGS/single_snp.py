#run at 'Project/METAMAP/notebook/RapMapTest/Pipelines'

import os,sys
sys.path+=['/cellar/users/btsui/Project/METAMAP/notebook/RapMapTest/Pipelines/']
import pandas as pd
import subprocess
from multiprocessing import Process
import param

def startChildren(cmd):
    def f():
        os.system(cmd) 
        #p.close()
    p = Process(target=f)
    p.start()
    return p

TEST=False

if TEST:
    srrRun='SRR961660'
    specie='Homo_sapiens'
    downloadSpeed='2000000'
else:
    srrRun=sys.argv[1]
    specie=sys.argv[2]
    downloadSpeed='200000'

print srrRun,specie
#baseGenomesDir='/cellar/users/btsui/Data/BOWTIE_GENOME_SNP_INDEX/'
baseGenomesDir='/cellar/users/btsui/Data/BOWTIE_GENOME_SNP_INDEX/'

log_out_dir=param.log_out_dir#'/cellar/users/btsui/Data/SRA/all_seq/log/'
count_out_dir=param.count_out_dir#'/cellar/users/btsui/Data/SRA/all_seq/chip/'
genomeDir=baseGenomesDir+specie+'/'
tmp_dir="/tmp/SRA_DATA/"

count_script_dir='/cellar/users/btsui/Project/METAMAP/notebook/RapMapTest/Chip-seq/count'
SRA_FASTQ_TOOL_DIR="/cellar/users/btsui/Program/SRA_TOOL_KIT/sratoolkit.2.4.2-ubuntu64/bin/fastq-dump.2.4.2"
myoption=r'"/cellar/users/btsui/.aspera/connect/bin/ascp|/cellar/users/btsui/.aspera/connect/etc/asperaweb_id_dsa.openssh"'
bam_read_count_dir='/cellar/users/btsui/Program/bam_read_count/bam-readcount-master/bin/bam-readcount'

trim_galore_Dir='/cellar/users/btsui/Program/TRIMAGLORE//trim_galore'
base_sra_dir='/tmp/btsui/METH/sra/'

##make temperoary directory
job_tmp_dir=tmp_dir+srrRun+"/"
subprocess.call(["rm", "-rf",job_tmp_dir])#remove the directory before running STAR
subprocess.call(["mkdir", "-p",job_tmp_dir]) #tmp dir for processing
os.chdir(job_tmp_dir)
##download sra file
downloadCommand=['prefetch','-t','ascp','--ascp-path',myoption,' --ascp-options "-l {max_traffic}" '.format(max_traffic=downloadSpeed),srrRun]
os.system(' '.join(downloadCommand))

##identify adaptor contents using first 10000 reads
myCmd='{sra_dump_dir} --stdout {sra_file_dir} |head -n 10000 > head.fq'.format(sra_dump_dir=SRA_FASTQ_TOOL_DIR,                                    sra_file_dir=base_sra_dir+srrRun+'.sra',trim_galore_Dir=trim_galore_Dir)
os.system(myCmd) 
os.system(trim_galore_Dir+' '+'head.fq')
##identify adaptor contents
fq_trimming_report_S=pd.Series.from_csv('head.fq_trimming_report.txt',index_col=None,sep='\t\t\t\t\\t\t\tt')
adapter_sequence=fq_trimming_report_S.str.extract("Adapter sequence: '(\w+)'",expand=False).dropna().iloc[0]
##set up pipe for counting the data
##remove pipes if they exist 
os.system('rm {srrRun}_bowtie_in  {srrRun}_bowtie_out'.format(srrRun=srrRun))#{srrRun}_bowtie_out, file_sorted
os.system('mkfifo {srrRun}_bowtie_in   {srrRun}_bowtie_out'.format(srrRun=srrRun))#{srrRun}_bowtie_out,file_sorted

if TEST:
    cmd_4="genomeCoverageBed -ibam file_sorted -bg| awk '{ if ($4 >= 1) { print } }' >out.bg"
else:
    cmd_4="genomeCoverageBed -ibam file_sorted -bg| awk '{ if ($4 >= 5) { print } }' >out.bg"
cmd_0='samtools view -bS {srrRun}_bowtie_out | samtools sort -  > file_sorted'.format(srrRun=srrRun)
cmd_1='bowtie2  -x {ref} -U {srrRun}_bowtie_in --no-unal --threads 64 > {srrRun}_bowtie_out 2>bowtie_log.txt'.format(ref=genomeDir,srrRun=srrRun)
#take in and sort it 
if TEST:
    cmd_2_fmt='{sra_dump_dir} --stdout {sra_file_dir} | head -n 400000 |cutadapt -a {adapter_sequence_1} - > {srrRun}_bowtie_in'
else:
    cmd_2_fmt='{sra_dump_dir} --stdout {sra_file_dir} |cutadapt -a {adapter_sequence_1} - > {srrRun}_bowtie_in'
    
cmd_2=cmd_2_fmt.format(
 sra_file_dir=base_sra_dir+srrRun+'.sra',srrRun=srrRun,adapter_sequence_1=adapter_sequence,sra_dump_dir=SRA_FASTQ_TOOL_DIR)
###execute code
my_p_l=[startChildren(cmd_0), startChildren(cmd_2)]

os.system(cmd_1)

###index and identify the regions of interest
os.system('samtools index file_sorted')
fa_dir='/cellar/users/btsui/Data/ensembl/release/fasta/Homo_sapiens.GRCh38.dna_rm.toplevel.fa'
snpBed='/cellar/users/btsui/Data/dbsnp/snp_beds/Homo_sapiens.bed'
cmd_5=bam_read_count_dir+' -l '+snpBed+' -f '+fa_dir+' file_sorted |gzip > snp.txt.gz'
os.system(cmd_5)

os.system('echo ">>>>bowtie2 log" >log.txt')
os.system('tail -n 10 bowtie_log.txt >>log.txt')
os.system('echo ">>>>head.fq_trimming_report.txt">>log.txt')
os.system('cat head.fq_trimming_report.txt >> log.txt')
os.system('cp log.txt {log_out_dir}/{srrRun}.log'.format(log_out_dir=log_out_dir,
                                                        srrRun=srrRun))

"""
#old code
print cmd_0
print cmd_1
print cmd_2
#cmd_2, cut adapt, to bowtie, 
my_p_l=[startChildren(cmd_0),startChildren(cmd_1),startChildren(cmd_2)]
os.system(cmd_4)
tmp_cmd='gzip -c out.bg >  {count_out_dir}/{srrRun}.bg.gz'.format(count_out_dir=count_out_dir,srrRun=srrRun)

os.system(tmp_cmd)

os.system('echo ">>>>bowtie2 log" >log.txt')
os.system('tail -n 10 bowtie_log.txt >>log.txt')
os.system('echo ">>>>head.fq_trimming_report.txt">>log.txt')
os.system('cat head.fq_trimming_report.txt >> log.txt')
os.system('cp log.txt {log_out_dir}/{srrRun}.log'.format(log_out_dir=log_out_dir,
                                                        srrRun=srrRun))


#os.system('gzip -c out.bg > {count_out_dir}/{srrRun}.bg.gz'.format(
#    count_out_dir=count_out_dir,srrRun=srrRun))
os.system('rm -r '+job_tmp_dir)
os.system('rm '+base_sra_dir+srrRun+'.sra')
os._exit(0)
"""