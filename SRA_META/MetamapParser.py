__author__ = 'btsui'
import xml.etree.ElementTree as ET
#import sharedFunctionParsing as shp
import os
import sys
import pandas as pd
class MetamapParse:
    outputPostfix='.out.npy'
    inputPostfix='.out'
    def __init__(self):
        return

    """
    for each record
    get biosample Id, CUI
    """
    #output,

    def praseCandidate(self,Candidate):
        UMLS= Candidate.find('CandidateCUI').text
        score= int(Candidate.find('CandidateScore').text)
        return UMLS,score

    def parseRecord(self,MMO, parseCandidateFunction):
        Utterances= MMO.find('Utterances')
        IdText=Utterances.find('Utterance/Phrases/Phrase/PhraseText')
        BioSampleId=IdText.text.replace(',','')
        umlsContectDict={}
        for Utterance in  Utterances.findall('Utterance'): #Find entry of interest
            Phrases= Utterance.find('Phrases')
            
            for Phrase in Phrases:
                for Candidates in Phrase.findall('Candidates'):
                    for Candidate in  Candidates.findall('Candidate'):
                        parseCandidateFunction(Candidate)
                        UMLS,content=parseCandidateFunction(Candidate)
                        if Candidate.find('Status').text=='0':
                            umlsContectDict[UMLS]=content
        return BioSampleId, umlsContectDict
    """
                def parseTree(self,InF):
                    tree=ET.parse(InF)
                    #tree=ET.iterparse(InF)
                    root = tree.getroot()
                    myBioSampleDict={}
                    for MMO in root.findall('MMO'): #replace MMO for record title
                        BioSampleId, umlsContectDict=self.parseRecord(MMO,self.praseCandidate)
                        myBioSampleDict[BioSampleId]=umlsContectDict
                        #break
                    return myBioSampleDict
    """
    def parseTree(self,InF):
        #tree=ET.parse(InF)
        myIter=ET.iterparse(InF)
        #tree=ET.iterparse(InF)
        #root = tree.getroot()
        myBioSampleDict={}
        for i ,(start_end,obj) in enumerate(myIter):
            if obj.tag=='MMO':
                MMO=obj
                BioSampleId, umlsContectDict=self.parseRecord(MMO,self.praseCandidate)
                myBioSampleDict[BioSampleId]=umlsContectDict
                obj.clear()
                #if i >5000:###test
                #	break

        return myBioSampleDict
    def process(self,InF):
        myParsedDict=self.parseTree(InF)
        srsLevel=[]
        attribLevel=[]
        cuiScores=[]

        for srsKey, CUIScoreDict in myParsedDict.iteritems():
            for CUI,score in CUIScoreDict.iteritems():
                srsLevel.append(srsKey)
                attribLevel.append(CUI)
                cuiScores.append(score)
        multI=pd.MultiIndex.from_arrays([ srsLevel,attribLevel])
        combinedSeries=pd.Series(data=cuiScores,index=multI)
        combinedSeries.to_pickle(InF+'.npy')
        
if __name__=='__main__':

    fname=sys.argv[1]
    p=MetamapParse()
    p.process(fname+p.inputPostfix)
