__author__ = 'btsui'
import os
import UMLSParam as param
import pandas as pd
class UMLS:
    umlsToEng=None
    def __init__(self):
        if not os.path.isfile(param.umlsEngSName):
            print 'init'
            import MySQLdb
            mysql_cn= MySQLdb.connect(host='avesso',
                port=3306,user='btsui', passwd='password',
                db='umls')
            myTable=pd.read_sql("select * from MRCONSO where STT='PF' and TS='P' and LAT='ENG' and ISPREF='Y'", con=mysql_cn)
            s=myTable.set_index('CUI').STR
            s.to_pickle(param.umlsEngSName)
        self.umlsToEng=pd.read_pickle(param.umlsEngSName)
    def convertIdsToEng(self,ids):
        return self.umlsToEng[ids]