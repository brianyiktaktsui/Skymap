__author__ = 'btsui'
import sharedVariable as shv
embryo=False
pos= '.embryo' if embryo else ''
edgeListDir=shv.baseMetaDataDir+'NCITerminology.edgelist.nodefilter.csv'
#cellDir=shv.baseMetaDataDir+'NCITerminology.enriched.pyc'+pos
cleanIdDir=shv.baseMetaDataDir+'NCIIdToEngS.pyc'+pos
idToUMLSDir=shv.baseMetaDataDir+'NCIIdToUMLSS.pyc'
relToEngDir=shv.baseMetaDataDir+'NCIRelToEng.pyc'
