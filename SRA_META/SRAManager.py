#
__author__ = 'btsui'

import SRAParam
from clusterBaseClass import clusterBaseClass
import mergeSRAResults as Merger
import os
import SRAParser


class SRAMangaer(clusterBaseClass):
    className = 'SRAMangaer'

    def __init__(self):
        clusterBaseClass.__init__(self,
                                  outputPostfix=SRAParser.SRAParser.outputPostfix,
                                  baseSplitDir='/cellar/users/btsui/Data/nrnb01_nobackup/tmp/METAMAP//splittedInput_' + self.className + '_',
                                  pythonScriptName='/cellar/users/btsui/Project/METAMAP/code/metamap/SRAParser.py',
                                  CWD='/cellar/users/btsui/Project/METAMAP/code/metamap',
                                  minCorrectSize=0,
                                  memory=2,
                                  smp=1
                                  )

    def run(self, inputFDir, outDir):
        # consist of both input for clustering
        fname = inputFDir.split('/')[-1]
        self.splitOutDir = self.baseSplitDir + fname + '/'
        print 'splitting input'
        #termToId = LS.split(inputFDir, self.nFiles, self.splitOutDir, clean=True)  # retain signature
        self.setNFiles(SRAParam.nConcurJob)
        if os.path.exists(self.splitOutDir ):
            os.system('rm '+self.splitOutDir +'/*')
        else:
            os.mkdir(self.splitOutDir )
        if not self.Done():
            # fname,nfiles,splitOutDir
            self.processUntilAllDone()

        Merger.runMerger( self.splitOutDir, outDir=outDir)


if __name__ == '__main__':
    # '.realign.spliceVariantMaxMatrix'


    outDir = '/cellar/users/btsui/Data/nrnb01_nobackup/METAMAP/' +'SRA_parse'

    m = SRAMangaer()
    m.run(SRAParam.SRADir, outDir=outDir)
