"""
merge all the files together
"""
import os
import SRAParser
def runMerger(splitOutDir, outDir):
    """

    :param splitOutDir:
    :param outDir:
    :return:
    """
    with open(outDir,'w')as outF:
        fnames=os.listdir(splitOutDir)
        partialResultFanmes=filter(lambda fname:fname.endswith(SRAParser.SRAParser.outputPostfix),fnames)
        outF.write("\t".join(['type', 'accession', 'annot']) + '\n')
        for partialResultFanme in partialResultFanmes:
            with open(splitOutDir+'/'+partialResultFanme,'r') as partF:
                partF.readline()
                for l in partF:
                    outF.write(l)





    #for all files with extension, merge them together

if __name__=='__main__':
    splitOutDir='/cellar/users/btsui/Data/nrnb01_nobackup/tmp/METAMAP/splittedInput_SRAMangaer_'
    outDir='/cellar/users/btsui/Data/nrnb01_nobackup/tmp/METAMAP/SRA.scientific.txt'
    runMerger(splitOutDir,outDir)