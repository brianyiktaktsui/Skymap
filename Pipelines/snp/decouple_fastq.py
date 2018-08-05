#!/cellar/users/btsui/anaconda2/bin/python
import sys
fname=sys.argv[1]
r1=open(fname+'_R1','w')
r2=open(fname+"_R2",'w')
with open (fname,'r') as f:
    for i,l in enumerate(f):
        if ((i/4)%2)==0:
            r1.write(l)
        else:
            r2.write(l)
r1.close()
r2.close()