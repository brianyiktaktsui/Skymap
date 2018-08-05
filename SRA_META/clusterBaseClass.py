__author__ = 'btsui'
import os
import time
import subprocess as sp

"""
name of the file should match the job number
"""

class clusterBaseClass:

    baseSplitDir=None
    splitOutDir=None
    errorOutputDir='/cellar/users/btsui/Data/nrnb01_nobackup/METAMAP/sgeErr/'
    outDir='/cellar/users/btsui/Project/METAMAP/sgeOut/'
    TEST=False
    nFiles=2 if TEST else 50 #150
    userNCores=None
    userMem=None
    outputPostfix=None
    scriptName=None
    CWD=None
    maxRun=None
    bashScriptName='metamapWrapper.sh'
    """
    check all all the process are done
    input: splittedFiles
    output: True/Flase: True if all processed
    """
    def __init__(self,outputPostfix,baseSplitDir,pythonScriptName,CWD,minCorrectSize,memory=1,smp=17,maxRun=5):
        self.outputPostfix=outputPostfix
        self.baseSplitDir=baseSplitDir
        self.PY_SCRIPT_NAME=pythonScriptName
        self.CWD=CWD
        self.minCorrectSize=minCorrectSize
        self.memory=memory
        self.smp=smp
        self.maxRun=maxRun
    def Done(self):
        """
        processing until done
        condition: no jobs on qstat
        """
        if not os.path.isdir(self.splitOutDir):
            return False

        outputFiles=map (lambda i:str(i)+self.outputPostfix,range(1, self.nFiles+1)) # all the files should be contiguous from 1 to n+1 job
        #print outputFiles

        return all(map( lambda outF:outF in set(os.listdir(self.splitOutDir)) and os.stat(self.splitOutDir+outF).st_size>(300 if self.TEST else self.minCorrectSize) , outputFiles ))

        #all(map( lambda outF:outF in set(os.listdir(self.splitOutDir)) and os.stat(self.splitOutDir+outF).st_size>(300 if self.TEST else self.minCorrectSize) , outputFiles ))


    def fileProcessedStatus(self,inF):
        """
        fname: file to check if processed correctly
        return: True/ False
        """
        return ( inF in set(os.listdir(self.splitOutDir)) and os.stat(self.splitOutDir+inF).st_size>(300 if self.TEST else self.minCorrectSize))

    def remainingJobNumber(self):
        outputFiles=map (lambda i:str(i)+self.outputPostfix,range(1, self.nFiles+1))
        unprocessedFiles=filter( lambda outF: not self.fileProcessedStatus(outF) , outputFiles )
        unprocessedJobNumbers=map( lambda fname: int ( fname.split('/')[-1].replace(self.outputPostfix,'') ),unprocessedFiles)
        return unprocessedJobNumbers

    def jobsOnQstat(self):
        rawOut=sp.check_output(['qstat'])
        return any(map(lambda l: self.bashScriptName[:8] in l, rawOut.split('\n')))
    """
    qsub the script to cluster
    input: splitted dir, number
    """
    def returnFiles(self):
        outputFiles=map (lambda i:str(i)+self.outputPostfix,range(1, self.nFiles))
        return outputFiles
    def setNFiles(self,nFiles):
        self.nFiles=nFiles
    def submitToCluster(self):

        bashParam={'SPLIT_INPUT_DIR':self.splitOutDir,
                   'CWD':self.CWD,
                   'SCRIPT_NAME':self.PY_SCRIPT_NAME
                   }
        remainingJobsId=self.remainingJobNumber()
        print 'number of jobs remaining: ',len(remainingJobsId),'\n'
        bashParamStr=','.join(map(lambda (k,v):k+'='+str(v) ,bashParam.iteritems()))
        for id in remainingJobsId:
            myCommandDict={
                           '-t': str(id),
                           '-tc':self.nFiles,
                           '-l':'h_vmem='+str(self.memory)+'g',
                           '-pe smp':self.smp,
                           '-p':0,
                           #'-o':self.outDir,
                           '-e':self.errorOutputDir
                           #script name
                           }
            paramString=reduce(lambda a,(k,v):a+' '+k+' '+str(v) ,myCommandDict.iteritems(), "")
            command ='qsub '+'-v '+bashParamStr+paramString+' '+self.bashScriptName
            os.system(command)
        #/submitting job
        #print command
        #map(lambda fname:os.remove(self.errorOutputDir+fname) ,os.listdir(self.errorOutputDir))
        map(lambda fname:os.remove(self.outDir+fname) ,os.listdir(self.outDir))

    def processUntilAllDone(self):
        runsSoFar=0
        while not self.Done() and runsSoFar<self.maxRun:
            if self.jobsOnQstat():
                print '.'
            else:
                self.submitToCluster()
                runsSoFar+=1
            time.sleep(2.0)
