#!/cellar/users/btsui/anaconda2/bin/python
import fileinput
import sys
"""
stdin: read all the files
stdout: output all the non-zeo data
"""
for line in fileinput.input():
    splitL=line.split('\t')
    if float(splitL[4])>=10.0:
        sys.stdout.write('\t'.join(splitL[:3]+[splitL[4]]))
    