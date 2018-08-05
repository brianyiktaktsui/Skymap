import xml.etree.ElementTree as ET
import os
import pandas as pd
import time
import sys
import SRAParam
class SampleParser:
    singleAttrib=['TITLE','DESCRIPTION','SCIENTIFIC_NAME','SUBMITTER_ID']
    attribName='SAMPLE_ATTRIBUTE'
    recordName='SAMPLE'
    f_extd='.sample.xml'
    def parseSample(self,sample):
        keys=[]
        vals=[]
        for myAttrib in self.singleAttrib:
            Iter=sample.iter(myAttrib)
            try:
                val=Iter.next().text
            except StopIteration:
                continue
            if val !=None and myAttrib !=None:
                keys.append(myAttrib),vals.append(val.replace('\t',''))
        for sample_attrib in sample.iter(self.attribName):
            val=sample_attrib.findtext('VALUE')
            if val!=None:
                keys.append(sample_attrib.findtext('TAG'))
                vals.append(val.replace('\t',''))
        return keys,vals
    def parseFile(self,fdir):
        cumAccessions,cumKeys,cumVals=[],[],[]
        root=ET.parse(fdir).getroot()
        for s in root.findall(self.recordName):
            accession=s.attrib['accession']
            keys,vals=self.parseSample(s)
            accessions=[accession]*len(keys)
            cumAccessions+=accessions
            cumKeys+=keys
            cumVals+=vals
        return cumAccessions,cumKeys,cumVals
    def parseFiles(self,sras,inDir):
        MultCumAccessions,MultCumKeys,MultCumVals=[],[],[]
        for sra in sras:
            fullDir=inDir+'/'+sra+'/'+sra+self.f_extd
            if os.path.isfile(fullDir):
                cumAccessions,cumKeys,cumVals=self.parseFile(fullDir)
                MultCumAccessions+=cumAccessions
                MultCumKeys+=cumKeys
                MultCumVals+=cumVals
        srsToKeyI=pd.MultiIndex.from_tuples(zip(MultCumAccessions,MultCumKeys))
        multIS=pd.Series(data=MultCumVals,index=srsToKeyI)
        return multIS

class ExperimentParser:
    singleAttrib=['TITLE','DESIGN_DESCRIPTION','LIBRARY_STRATEGY','LIBRARY_SOURCE','LIBRARY_SELECTION']
    attribName='EXPERIMENT_ATTRIBUTE'
    recordName='EXPERIMENT'
    f_extd='.experiment.xml'
    def parseSample(self,sample):
        keys=[]
        vals=[]
        for myAttrib in self.singleAttrib:
            Iter=sample.iter(myAttrib)
            try:
                val=Iter.next().text
            except StopIteration:
                continue
            if val !=None and myAttrib !=None:
                keys.append(myAttrib),vals.append(val.replace('\t',''))
                #print myAttrib,val.replace('\t','')
        #extract the layout
        Iter=sample.iter('LIBRARY_LAYOUT')
        tmp=Iter.next()
        children=iter(tmp).next()
        keys.append('LIBRARY_LAYOUT'),vals.append(children.tag)
        #print children
        #print '\t'.join(map(str,[,children.text,children.items(),children.attrib,children.keys()]))
        #print 
        for sample_attrib in sample.iter(self.attribName):
            val=sample_attrib.findtext('VALUE')
            if val!=None:
                keys.append(sample_attrib.findtext('TAG'))
                vals.append(val.replace('\t',''))
        return keys,vals
    def parseFile(self,fdir):
        cumAccessions,cumKeys,cumVals=[],[],[]
        root=ET.parse(fdir).getroot()
        for s in root.findall(self.recordName):
            accession=s.attrib['accession']
            keys,vals=self.parseSample(s)
            accessions=[accession]*len(keys)
            cumAccessions+=accessions
            cumKeys+=keys
            cumVals+=vals
        return cumAccessions,cumKeys,cumVals
    def parseFiles(self,sras,inDir):
        MultCumAccessions,MultCumKeys,MultCumVals=[],[],[]
        for sra in sras:
            fullDir=inDir+'/'+sra+'/'+sra+self.f_extd
            if os.path.isfile(fullDir):
                cumAccessions,cumKeys,cumVals=self.parseFile(fullDir)
                MultCumAccessions+=cumAccessions
                MultCumKeys+=cumKeys
                MultCumVals+=cumVals
        srsToKeyI=pd.MultiIndex.from_tuples(zip(MultCumAccessions,MultCumKeys))
        multIS=pd.Series(data=MultCumVals,index=srsToKeyI)
        return multIS

class SRAParser:
    outputPostfix = '.srx.pickle' #just put one of them out there
    outputPostfix2='.srs.pickle'
    inputPostfix = ''

    def __init__(self):
        return


    def process(self,inDir):
        chunkNum=int( inDir.split('/')[-1])#the number indicate the chunk of files to be processed
        allSra=os.listdir(SRAParam.SRADir)
        chunkSize=len(allSra)/SRAParam.nConcurJob
        print (chunkSize)
        sras=allSra[(chunkNum*chunkSize):((chunkNum+1)*chunkSize)]
        #with open(inDir+self.outputPostfix,'w') as f:
        print (sras)
        exprS = ExperimentParser().parseFiles(sras, SRAParam.SRADir)
        sampleS=SampleParser().parseFiles(sras,SRAParam.SRADir)

        exprS.to_pickle(inDir+self.outputPostfix)
        sampleS.to_pickle(inDir+self.outputPostfix2)
            #f.write("\t".join(['type','accession','annot'])+'\n')
        """
        for mySra in mySubset:
            exprDir= SRAParam.SRADir+mySra+'/'+mySra+'.experiment.xml'
            sampleDir= SRAParam.SRADir+mySra+'/'+mySra+'.sample.xml'

            if os.path.isfile(exprDir) and os.path.isfile(sampleDir): #confirm the study is well annotated
                    exprTokens=self.parseExpr(exprDir)
                    sampleTokens= self.parseSample(sampleDir)
                    if len(exprTokens)>0:
                        f.write('\n'.join(map(lambda myTuple:'\t'.join(myTuple), exprTokens))+'\n')
                    if len(sampleTokens)>0:
                        f.write('\n'.join(map(lambda myTuple:'\t'.join(myTuple), sampleTokens))+'\n')
        """
if __name__=='__main__':

    fname=sys.argv[1]
    #fname = '/cellar/users/btsui/Data/nrnb01_nobackup/METAMAP/test/1'
    # let the fname decide what to put
    p = SRAParser()
    p.process(fname)
