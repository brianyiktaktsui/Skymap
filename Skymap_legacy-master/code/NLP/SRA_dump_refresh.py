
# coding: utf-8

# In[4]:

import pandas as pd
import os
from ftplib import FTP
ftpLink='ftp.ncbi.nlm.nih.gov'
myRemoteDir='sra/reports/Metadata/'
ftp = FTP(ftpLink)
ftp.login()
ftp.cwd(myRemoteDir)
fnames=pd.Series(ftp.nlst())
#sort the data numerically
myFullSraMeta=fnames[fnames.str.contains('NCBI_SRA_Metadata_Full')
      ].sort_values().iloc[-1]

myDownloadFnames=['SRA_Accessions.tab',myFullSraMeta,
                  'SRA_Run_Members.tab']


# ### pull all the data

# In[5]:

os.system('rm -r '+bdir+'*')


# In[6]:

bdir='/cellar/users/btsui/Data/SRA/DUMP/'
for f in myDownloadFnames:
    fileDir = bdir+f
    File=open(fileDir,'wb')
    ###reopen ftp everytime to avoid idling 
    ftp = FTP(ftpLink)
    ftp.login()
    ftp.cwd(myRemoteDir)
    ftp.retrbinary('RETR %s' % f, File.write)
    File.close()


# ### untar the data into the right directory

# In[7]:

os.chdir(bdir)


# In[10]:

tarFmt='tar -xvf {inDir} -C {outDir}'


# In[25]:

fullMetaUntarDir=bdir+'FULL_SRA_meta/'


# In[26]:

os.system('mkdir '+fullMetaUntarDir)


# In[27]:

tarCmd=tarFmt.format(inDir=bdir+myFullSraMeta,
             outDir=fullMetaUntarDir)


# In[ ]:

os.system(tarCmd)


# ### rename to directory of full meta to something generic

# In[33]:

untarredDir=os.listdir(fullMetaUntarDir)[0]


# In[42]:

mvFmt='mv {src} {dest}'


# In[45]:

mvCmd=mvFmt.format(src=fullMetaUntarDir+untarredDir,dest=fullMetaUntarDir+'SRA_META')


# In[46]:

os.system(mvCmd)


# In[ ]:



