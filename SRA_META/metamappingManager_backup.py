#
__author__ = 'btsui'
from inputPartitionerText import inputPartitionerText
import os
from metamapping import Metamap
import time
import subprocess as sp
class metamappingManager:
    nFiles=150
    baseSplitDir='/cellar/users/btsui/Data/nrnb01_nobackup/METAMAP/splittedInput_'
    splitOutDir=None
    errorOutputDir='/cellar/users/btsui/Project/METAMAP/sgeErr/'
    outDir='/cellar/users/btsui/Project/METAMAP/sgeOut/'
    TEST=False
    outputPostfix=Metamap.outputPostfix

    """
    check all all the process are done
    input: splittedFiles
    output: True/Flase: True if all processed
    """
    def Done(self,splittedFiles=None):
        if not os.path.isdir(self.splitOutDir):
            return False
        outputFiles=map (lambda i:str(i)+self.outputPostfix,range(1, self.nFiles))if splittedFiles==None else map(lambda s:s+self.outputPostfix,splittedFiles)
        return all(map( lambda outF:outF in set(os.listdir(self.splitOutDir)) and os.stat(self.splitOutDir+outF).st_size>5000, outputFiles ))
    """
    processing until done
    condition: no jobs on qstat
    """
    def jobsOnQstat(self):
        rawOut=sp.check_output(['qstat'])
        return any(map(lambda l: Metamap.scriptName[:9] in l, rawOut.split('\n')))
    """
    qsub the script to cluster
    input: splitted dir, number
    """
    def submitToCluster(self):
        memory=1
        SCRIPT_NAME='metamapping.py'
        bashParam={'SPLIT_INPUT_DIR':self.splitOutDir,
                   'CWD':'/cellar/users/btsui/Project/METAMAP/code/metamap/',
                   'SCRIPT_NAME':SCRIPT_NAME
                   }

        bashParamStr=','.join(map(lambda (k,v):k+'='+str(v) ,bashParam.iteritems()))
        myCommandDict={
                       '-t':'1-'+str(self.nFiles),
                       '-tc':50,
                       '-l':'h_vmem='+str(memory)+'g',
                       '-pe smp':17,
                       #'-o':self.outDir,
                       '-e':self.errorOutputDir
                       #script name
                       }
        paramString=reduce(lambda a,(k,v):a+' '+k+' '+str(v) ,myCommandDict.iteritems(), "")
        command ='qsub '+'-v '+bashParamStr+paramString+' '+Metamap.scriptName
        print command
        map(lambda fname:os.remove(self.errorOutputDir+fname) ,os.listdir(self.errorOutputDir))
        map(lambda fname:os.remove(self.outDir+fname) ,os.listdir(self.outDir))
        os.system(command)
    def processUntilAllDone(self,splittedFiles):
        while not self.Done(splittedFiles):
            if self.jobsOnQstat():
                print '.'
            else:
                self.submitToCluster()
            time.sleep(2.0)

    def run(self,inputFDir):
        fname=inputFDir.split('/')[-1]
        self.splitOutDir=self.baseSplitDir+fname+'/'
        if not self.Done():
            LS=inputPartitionerText()
            #fname,nfiles,splitOutDir
            print 'splitting input'
            splittedFiles=LS.split(inputFDir,self.nFiles,self.splitOutDir,clean=self.TEST)
            self.processUntilAllDone(splittedFiles)

if __name__=='__main__':
    fname='/cellar/users/btsui/Data/nrnb01_nobackup/METAMAP/input/allBioSample.mouse.human.csv'
    m=metamappingManager()
    m.run(fname)
