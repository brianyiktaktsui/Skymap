import pandas as pd
import sys
import os
import time

## program directories
bam_read_count_dir='/cellar/users/btsui/Program/bam_read_count/bam-readcount-master/bin/bam-readcount'

##output directories
snp_out_dir='/nrnb/users/btsui/Data/tcga_extracted_lgg_snp_from_aligned_tcga_bam/'

##base temporary output directories
out_dir='/tmp/'

#i=0
i=int(sys.argv[1])-1

#input directories
token_dir='/cellar/users/ramarty/tokens/gdc-user-token.2018-06-25T22_21_40.089Z.txt'
manifest_dir='/cellar/users/btsui/Project/METAMAP/notebook/RapMapTest/XGS_WGS/tcga_lgg_wgs_bams.df.wxs_rnaseq.pickle'

gdc_cmd_fmt='gdc-client download -t {token_dir} -d {out_dir} {file_uuid}'

### download from TCGA
manifest_df=pd.read_pickle(manifest_dir)
manifest_S=manifest_df.iloc[i]

file_uuid=manifest_S['file_id']
print ('UUID: ',file_uuid)
gdc_cmd=gdc_cmd_fmt.format(out_dir=out_dir,file_uuid=file_uuid,token_dir=token_dir)

result = os.system(gdc_cmd)

###change to current dir
tmpDir=out_dir+file_uuid+'/'
os.chdir(tmpDir)

###extract using bam read count
cmd_bam_read_count=bam_read_count_dir+' -w 0 {file_name} |gzip > {snp_out_dir}/{file_uuid}.snp.txt.gz'.format(file_name=manifest_S['file_name'],file_uuid=file_uuid,snp_out_dir=snp_out_dir)

os.system(cmd_bam_read_count)
os.system('rm -r '+tmpDir)