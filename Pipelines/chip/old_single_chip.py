#run at 'Project/METAMAP/notebook/RapMapTest/Pipelines'

import os,sys
import pandas as pd
import subprocess
from multiprocessing import Process
import param
def stratChildren(cmd):
    def f():
        os.system(cmd) 
    p = Process(target=f)
    p.start()
    return p
TEST=False

#srrRun=sys.argv[1]
srrRun='SRR458459'
#specie=sys.argv[2]
specie='Homo_sapiens'
print srrRun,specie
baseGenomesDir='/cellar/users/btsui/Data/BOWTIE2_GENOME_INDEX/'
#out_dir='
base_dict_dir='/cellar/users/btsui/Data/Project/Skymap/ChipSeq/empty_references/'
log_out_dir=param.log_out_dir#'/cellar/users/btsui/Data/SRA/all_seq/log/'
count_out_dir=param.count_out_dir#'/cellar/users/btsui/Data/SRA/all_seq/chip/'
genomeDir=baseGenomesDir+specie+'/'
tmp_dir="/tmp/SRA_DATA/"

count_script_dir='/cellar/users/btsui/Project/METAMAP/notebook/RapMapTest/Chip-seq/count'
SRA_FASTQ_TOOL_DIR="/cellar/users/btsui/Program/SRA_TOOL_KIT/sratoolkit.2.4.2-ubuntu64/bin/fastq-dump.2.4.2"
myoption=r'"/cellar/users/btsui/.aspera/connect/bin/ascp|/cellar/users/btsui/.aspera/connect/etc/asperaweb_id_dsa.openssh"'
trim_galore_Dir='/cellar/users/btsui/Program/TRIMAGLORE//trim_galore'
base_sra_dir='/tmp/btsui/METH/sra/'

##make temperoary directory
job_tmp_dir=tmp_dir+srrRun+"/"
subprocess.call(["rm", "-rf",job_tmp_dir])#remove the directory before running STAR
subprocess.call(["mkdir", "-p",job_tmp_dir]) #tmp dir for processing
os.chdir(job_tmp_dir)
##download sra file
downloadCommand=['prefetch','-t','ascp','--ascp-path',myoption,' --ascp-options "-l 200000" ',srrRun]
os.system(' '.join(downloadCommand))

##identify adaptor contents using first 10000 reads
myCmd='{sra_dump_dir} --stdout {sra_file_dir} |head -n 10000 > head.fq'.format(sra_dump_dir=SRA_FASTQ_TOOL_DIR,                                    sra_file_dir=base_sra_dir+srrRun+'.sra',trim_galore_Dir=trim_galore_Dir)
os.system(myCmd) 
os.system(trim_galore_Dir+' '+'head.fq')
##identify adaptor contents
fq_trimming_report_S=pd.Series.from_csv('head.fq_trimming_report.txt',index_col=None,sep='\t\t\t\t\\t\t\tt')
adapter_sequence=fq_trimming_report_S.str.extract("Adapter sequence: '(\w+)'",expand=False).dropna().iloc[0]

##remove pipes if they exist 
os.system('rm {srrRun}_bowtie {srrRun}_count'.format(srrRun=srrRun))
##make pipes
os.system('mkfifo {srrRun}_bowtie {srrRun}_count'.format(srrRun=srrRun))
##
my_dict_dir=base_dict_dir+specie+'.size.tsv'

##set up pipe for counting the data
#


cmd_0='{count_script_dir} {my_dict_dir} {srrRun}_count'.format(
    count_script_dir=count_script_dir,srrRun=srrRun,my_dict_dir=my_dict_dir)
#cmd_1='bowtie2  -x {ref} -U {srrRun}_bowtie --threads 4  > {srrRun}_count 2>bowtie_log.txt'.format(ref=genomeDir,srrRun=srrRun)
cmd_1='bowtie2  -x {ref} -U {srrRun}_bowtie --threads 4  > {srrRun}_count 2>bowtie_log.txt'.format(ref=genomeDir,srrRun=srrRun)
cmd_2='{sra_dump_dir} --stdout {sra_file_dir} |cutadapt -a {adapter_sequence} - > {srrRun}_bowtie'.format(
 sra_file_dir=base_sra_dir+srrRun+'.sra',srrRun=srrRun,adapter_sequence=adapter_sequence,sra_dump_dir=SRA_FASTQ_TOOL_DIR)
print cmd_0
print cmd_1
print cmd_2
my_p_l=[stratChildren(cmd_0),stratChildren(cmd_1)]
os.system(cmd_2)

os.system('echo ">>>>bowtie2 log" >log.txt')
os.system('tail -n 10 bowtie_log.txt >>log.txt')
os.system('tail -n 10 bowtie_log.txt >>log.txt')
os.system('echo ">>>>head.fq_trimming_report.txt">>log.txt')
os.system('cat head.fq_trimming_report.txt >> log.txt')
#os.system('gzip -c log.txt > ')
os.system('cp log.txt {log_out_dir}/{srrRun}.log'.format(log_out_dir=log_out_dir,
                                                        srrRun=srrRun))
'bowtie_log.txt '

os.system('gzip -c bin.count.txt > {count_out_dir}/{srrRun}.bin.count.txt.gz'.format(
    count_out_dir=count_out_dir,srrRun=srrRun))
#process_names=[' bowtie2-align-s','fastq-dump.2.4.', 'cutadapt', 'a.out']
#for process_name in process_names:
#    print os.system('pkill '+process_name)
os.system('rm -r '+job_tmp_dir)
os.system('rm '+base_sra_dir+srrRun+'.sra')
os._exit(0)