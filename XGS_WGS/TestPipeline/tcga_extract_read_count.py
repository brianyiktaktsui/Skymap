import pandas as pd
import sys


import os
#i=0
i=int(sys.argv[1])

manifest_dir='/cellar/users/btsui/Project/METAMAP/notebook/RapMapTest/XGS_WGS/./tcga_lgg_wgs_bams.df.pickle'
token_dir='/cellar/users/ramarty/tokens/gdc-user-token.2018-06-25T22_21_40.089Z.txt'
bam_read_count_dir='/cellar/users/btsui/Program/bam_read_count/bam-readcount-master/bin/bam-readcount'

gdc_cmd_fmt='gdc-client download -t {token_dir} -d {out_dir} {file_uuid}'
#the following was just tmp out dir
out_dir='/nrnb/users/btsui/Data/tcga_raw_lgg/'
snp_out_dir='/nrnb/users/btsui/Data/tcga_extracted_lgg_snp/'

manifest_df=pd.read_pickle(manifest_dir)
manifest_S=manifest_df.iloc[i]

file_uuid=manifest_S['file_id']
print ('UUID: ',file_uuid)

gdc_cmd=gdc_cmd_fmt.format(out_dir=out_dir,file_uuid=file_uuid,token_dir=token_dir)


result = os.system(gdc_cmd)

print ('time for alignent:',total)
### pipe the data
tmpDir=out_dir+file_uuid+'/'
os.chdir(tmpDir)

specie='Homo_sapiens'

snpBed='/cellar/users/btsui/Data/dbsnp/snp_beds/'+specie+'.bed.with_chr'
fa_dir='/cellar/users/btsui/Data/ensembl/snp_masked/'+specie+'.microbe.fa'
#cmd_bam_read_count=bam_read_count_dir+' -l '+snpBed+' {} |gzip > snp.txt.gz'.format(manifest_S['file_name'])

cmd_bam_read_count=bam_read_count_dir+' {} |gzip > {}'.format(manifest_S['file_name'],snp_out_dir+manifest_S['file_name'].replace('.bam','.snp.gz'))
os.system(cmd_bam_read_count)
