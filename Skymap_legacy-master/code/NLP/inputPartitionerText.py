__author__ = 'btsui'
from collections import defaultdict
import os
class inputPartitionerText:
    """
    input: file name, nfiles
    output: file names of the splitted files

    design:
        assign the file based on the value of (position mod nfiles)
    """
    def split(self,fname,nfiles,splitOutDir,clean=True):
        if clean:
            self.cleanDir(splitOutDir)
        #
        filesPerProcess=defaultdict(list)
        #partition files
        with open(fname) as f:
            for i,l in enumerate(f):
                filesPerProcess[(i%nfiles+1)].append(l.strip('\n'))
        #spit out files
        if not os.path.isdir(splitOutDir):
            os.mkdir(splitOutDir)

        for k, lines in filesPerProcess.iteritems():
            with open(splitOutDir+'/'+str(k),'w') as f:
                f.write('\n\n'.join(lines))
                f.write('\n\n')
        return map(lambda i:str(i), filesPerProcess.keys())
    def cleanDir(self,splitOutDir):
        print 'cleaning \n\n'
        map(lambda fname:os.remove(splitOutDir+fname) ,os.listdir(splitOutDir))

if __name__=='__main__':
    LS=inputPartitionerText()
    splitOutDir='/cellar/users/btsui/Data/nrnb01_nobackup/METAMAP/splittedInput/'
    #LS.cleanDir(splitOutDir)
    fname='/cellar/users/btsui/Data/nrnb01_nobackup/METAMAP/test.out'
    LS.split(fname,2,splitOutDir )