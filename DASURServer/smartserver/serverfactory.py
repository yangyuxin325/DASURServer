#coding=utf-8
#!/usr/bin/env python
'''
Created on 2016年8月10日

@author: sanhe
'''
from regionserver import RegionServer
from unitserver import UnitServer
from nodeserver import NodeServer
from smartclass.serialsearch import InitSerialNo

__all__ = ['CreateServer']

FACTORY = {'region' : RegionServer,
           'unit' : UnitServer,
           'node' : NodeServer
           }

def CreateServer(db, server_type):
    if server_type in FACTORY:
        if server_type != 'region':
            InitSerialNo(db)
        return FACTORY(server_type)
    