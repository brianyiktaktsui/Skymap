
# coding: utf-8

# In[1]:

### parse sam file input
### if too many reads unmapped
"""
Use only [] for indexing
"""
import sys
import pandas as pd
import os
#fname='out.sam'
fname=str(sys.argv[1])
#specie='Homo_sapiens'#
specie=str(sys.argv[2])
emptyPickleDir='/cellar/users/btsui/Data/Project/Skymap/ChipSeq/empty_references/'+specie+'.pickle'


# In[2]:

myCountS=pd.read_pickle(emptyPickleDir)


# In[4]:

"""
convert this to using cdef


##for the offset, use my_dict
##for my data 
"""
##open sam file


"""
read in the file using cin and create a c++ map 
"""
checkMark=100000
with open(fname,'r') as f:
    failedCount=0 
    for l in f:
        if l[0]!='@':
            break
    for i,l in enumerate(f):## use c to read it line by line 
        splitL=l.split('\t')
        start_loc=int(splitL[3])
        tlen=len(splitL[9])
        rname=splitL[2]
        if rname !='*':
            end_loc=start_loc+tlen
            binned_start_loc=int(start_loc/20.0)*20
            binned_end_loc=int(end_loc/20.0)*20
            #print start_loc,end_loc
            for i in range(binned_start_loc,binned_end_loc+1,20):
                #print (rname,i)
                myCountS[(rname,i)]+=1
        else:
            failedCount+=1
            if i==checkMark:
                frac=failedCount/float(checkMark)
                if frac>0.9:
                    break
        #tlen=  int(int(splitL[9])/20.0)*20
        #rname,pos,tlen=splitL[2],binnedLoc,splitL[9]
            
        


# In[8]:

nonZero_CountS=myCountS[myCountS!=0]


# In[12]:

nonZero_CountS.to_pickle('bin_count.pickle')

