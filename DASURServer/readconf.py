#coding=utf-8
#!/usr/bin/env python
'''
Created on 2016年8月10日

@author: sanhe
'''

import ConfigParser

cf = ConfigParser.ConfigParser()
cf.read('app.conf')
DBname = cf.get('DB', 'name')
DBpassword = cf.get('DB', 'password')
period_var = cf.get('period','min_variation')

def getRemoteUrl(ip):
    return "mysql://root:" + DBpassword + "@" + ip + "/" + DBname + "?charset=utf8"

def getSqlUrl():
        return "mysql://root:" + DBpassword + "@localhost/" + DBname + "?charset=utf8"