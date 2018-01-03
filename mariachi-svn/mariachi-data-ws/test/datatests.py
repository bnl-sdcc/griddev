'''
Unit tests for mariachiws/data.py
'''
import unittest
import datetime
from mariachiws.data import *


class DataTests(unittest.TestCase):
    
    def testSiteFileHandlerInit(self):
        self.sfh = SiteFileHandler(directory="./testsite")
        self.assertEqual(self.sfh.rootdir,'./testsite')
            
    def testGetFilteredFileList(self):
        '''
        Test filename filtering by date.
        '''
        self.starttime=datetime.datetime(2008, 2, 11, 13 , 1, 1, 1, None)
        self.endtime=datetime.datetime(2008, 2, 13, 13 , 1, 1, 1, None)
        self.sfh = SiteFileHandler(directory="./test/testsite")
        files = self.sfh._getFilteredFileList('counts',self.starttime, self.endtime)
        
        
        