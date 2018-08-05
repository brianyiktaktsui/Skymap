#run at '/cellar/users/btsui/Project/METAMAP/notebook/RapMapTest/Pipelines/'
import os,sys
sys.path+=['/cellar/users/btsui/Project/METAMAP/notebook/RapMapTest/Pipelines/RNAseq/']
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
#base_dict_dir='/cellar/users/btsui/Data/Project/Skymap/ChipSeq/empty_references/'
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
os.system('rm bowtie {srrRun}_count fq1 fq2'.format(srrRun=srrRun))
os.system('mkfifo bowtie {srrRun}_count fq1 fq2'.format(srrRun=srrRun))

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

#cmd_1='{bowtie2_dir}  -x {ref} --interleaved {srrRun}_bowtie --threads {nThread} > {srrRun}_count 2>bowtie_log.txt'.format(ref=genomeDir,srrRun=srrRun,nThread=nThread,bowtie2_dir=bowtie2_dir)
#take in and sort it 

RUN_FULL=True
if TEST and (RUN_FULL != True):
    cmd_2_fmt='{sra_dump_dir} --stdout --split-files {sra_file_dir} | head -n 8000 |cutadapt -m 31 --interleaved -a {adapter_sequence_1} -A {adapter_sequence_2} - > bowtie'
else:
    cmd_2_fmt='{sra_dump_dir} --stdout --split-files {sra_file_dir} |cutadapt --interleaved -m 31 -a {adapter_sequence_1} -A {adapter_sequence_2} - > bowtie'
    
cmd_2=cmd_2_fmt.format(
 sra_file_dir=base_sra_dir+srrRun+'.sra',srrRun=srrRun,adapter_sequence_1=adapter_sequence_1,adapter_sequence_2=adapter_sequence_2,sra_dump_dir=SRA_FASTQ_TOOL_DIR)

deinterleave_dir='/cellar/users/btsui/Project/METAMAP/notebook/RapMapTest/Pipelines/RNAseq/deinterleave_fastq.sh'
cmd_interleave=deinterleave_dir+'< bowtie fq1 fq2'
"""
scratch
"""
##### code specific to my data 
###execute code

kalisto_transcriptome_dir='/cellar/users/btsui/Data/kalisto_ref/'+specie

#cmd_1='{bowtie2_dir}  -x {ref} -U {srrRun}_bowtie_in --no-unal --threads {nThread} > {srrRun}_bowtie_out 2>bowtie_log.txt'.format(ref=genomeDir,srrRun=srrRun,nThread=nThread,bowtie2_dir=bowtie2_dir)
#take in and sort it 
"""
sailfish quant -i sfindex -l U -r <(gunzip -c reads.fq.gz) -o reads_quant

"""
#### parameter from : https://pachterlab.github.io/kallisto/starting
cmd_sailfish=" ".join(['/cellar/users/btsui/Program/kallisto',
                       'quant -i' ,kalisto_transcriptome_dir,
                       '-o','read_quant',
                       'fq1','fq2'
                      ])

my_p_l=[ startChildren(cmd_2),startChildren(cmd_interleave)]
os.system(cmd_sailfish)
#os.system(cmd_0)

os.system('gzip ./read_quant/abundance.tsv')
os.system('gzip ./read_quant/run_info.json')
os.system('cp ./read_quant/abundance.tsv.gz {count_out_dir}/{srrRun}.abundance.tsv.gz'.format(
    count_out_dir=count_out_dir,srrRun=srrRun))
os.system('cp ./read_quant/run_info.json.gz {count_out_dir}/{srrRun}.run_info.json.gz'.format(
    count_out_dir=count_out_dir,srrRun=srrRun))

os.system('rm -r '+job_tmp_dir)
os.system('rm '+base_sra_dir+srrRun+'.sra')
os._exit(0)
###index and identify the regions of interest
#os.system('samtools index file_sorted')
#os.system('samtools idxstats file_sorted |gzip> per_fa_record_stat.txt.gz')##ADDED
