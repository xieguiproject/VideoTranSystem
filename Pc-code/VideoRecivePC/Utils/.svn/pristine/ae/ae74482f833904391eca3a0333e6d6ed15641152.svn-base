import sys
import os
import configparser
from threading import Semaphore
class CONFIG(object):
    def __init__(self,configfile):
        self.config = configparser.ConfigParser()
        self.config.read(configfile)
        self.Sem = Semaphore(1)
        pass
    def getKeyValue(self,section,key):
        return self.config.get(section,key)
    def setKeyValue(self,section,key,value):
        pass
if __name__ == '__main__':
    config = CONFIG('config.ini')
    #print(config.getKeyValue('MySQL-Database','user'))