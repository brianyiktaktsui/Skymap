nnnq__author__ = 'btsui'

class CellOntologyFactory:
    """
    set myObo param
    """
    myObo='/cellar/users/btsui/Data/nrnb01_nobackup/METAMAP/input/cl.obo'
    myOutputPrefix='/cellar/users/btsui/Data/nrnb01_nobackup/METAMAP/input/cl'
    nSynonym=11
    mySynonymFileNames=None
    def deleteWeirdChars(self,text):
        return ''.join(ch for ch in text if ch.isalnum() or ch in ['_','-',' '])
    def parseRecord(self,record):
        """
        :param record: a term record
        :return: tuples
        """
        nonEmptyLines= filter(lambda s:s!='',record.split('\n') )
        noCommentLines=map(lambda s:s.split('!')[0],nonEmptyLines)
        return [ (l.split(": ")[0].replace(':','_'),l.split(": ")[1].replace(':','_')) for l in  noCommentLines if ': 'in l]
    def parseFile(self):
        with open (self.myObo) as f:
            records=f.read().split('[Term]')[1:]
        listOfRecord=map(self.parseRecord, records)
        notOboleteRecords=[record for record in listOfRecord if ('is_obsolete','true') not in record]
        #open mutliple files
        fileDict={i:open(self.myOutputPrefix+'.'+str(i),'w') for i in range(self.nSynonym)}#+1 is for name of term
        self.mySynonymFileNames=[self.myOutputPrefix+'.'+str(i) for i in range(self.nSynonym)]
        for record in listOfRecord:
            _,Id=filter(lambda (Type,text):Type=='id',record)[0]
            """
            for f in fileDict.values():
            wf.write(Id.replace(':','_')+', ')
            """
            texts=[text if Type !='synonym' else text.split('"')[1] for (Type,text) in record if Type in ['name','synonym']]
            for i ,text in enumerate(texts):
                if i<self.nSynonym:
                    cleanedText=self.deleteWeirdChars(text)
                    fileDict[i].write(Id.replace(':','_')+', ')
                    fileDict[i].write(cleanedText+', ')
                    fileDict[i].write('\n')
        for fobj in fileDict.values():
            fobj.close()
    def parseAndRun(self):
        self.parseFile()
        import os
        unprocessedFiles=filter( lambda fname:os.path.isfile(fname) ,self.mySynonymFileNames)
        for fname in  unprocessedFiles:
            'processing: ',fname
            import clusterRun
            clusterRun.runOnCluster(fname)
if __name__=='__main__':
    cellOntoFac=CellOntologyFactory()
    cellOntoFac.parseAndRun()


