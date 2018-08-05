#!/cellar/users/btsui/anaconda/bin/python
__author__ = 'btsui'
import metamappingManager as mm
import metamapParsingManager as mp
import mergeDF as mg
import os
def runOnCluster(fname):
    metamapManager=mm.metamappingManager()

    print '[PIPE] executing metamapping\n\n'
    metamapManager.run(fname)
    print '[PIPE] parsing metamap output\n\n'
    metamapParserManager=mp.metamappingParsingManager()
    metamapParserManager.run(fname)
    print '[PIPE] mergin metamap output\n\n'
    merger=mg.Merger()
    print metamapParserManager.splitOutDir,metamapManager.outputPostfix
    toMergeFnames=map( lambda i:metamapParserManager.splitOutDir+str(i)+metamapManager.outputPostfix,  range (1, metamapParserManager.nFiles+1 ) )
    merger.mergeDFs(toMergeFnames,fname)
    #metamapParser.parseDir(metamapManager.splitOutDir,fname)

if __name__=='__main__':
    fname='/cellar/users/btsui/Data/nrnb01_nobackup/METAMAP/input/allAttrib.v5.csv'
    runOnCluster(fname)
