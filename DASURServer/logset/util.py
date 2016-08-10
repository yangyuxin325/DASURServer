#coding=utf-8
#!/usr/bin/env python
'''
Created on 2016年3月2日

@author: sanhe
'''
from UserDict import UserDict

__all__ = ['StringReasonType', 'INSTRUCTIONS', 'def_refparam', 'def_refmodeparam',
           'def_refcondmodeparam', 'set_refparam', 'get_refparam', 'set_refmodeparam',
           'get_refmodeparam', 'set_refcondmodeparam', 'get_refcondmodeparam']

StringReasonType = {
                    'Data_Change_Cond':u'日期改变工况'
                    }

class Enum(set):
    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError

INSTRUCTIONS = Enum(['LED_AUTO', 'LED_ON','LED_OFF','LED_OFF',
                     'ON', 'OFF',
                     'gaosu', 'zhongsu', 'disu', 'tingzhi', 'fakai', 'faguan',
                     'zhileng', 'zhire', 'reshui', 'zl&rs', 'zr&rs',
                     'tongfeng', 'zidong'
                     ])

RefParam = UserDict()
RefModeParam = UserDict()
RefCondModeParam = UserDict()

def def_refparam(name, value):
    RefParam[name] = value
    
def def_refmodeparam(name, mode, value):
    RefModeParam[(name, mode)] = value
    
def def_refcondmodeparam(name, cond, mode, value):
    RefCondModeParam[(name, cond, mode)] = value
    
def set_refparam(name, value):
    if name in RefParam:
        RefParam[name] = value
    
def get_refparam(name):
    return RefParam.get(name)

def set_refmodeparam(name, mode, value):
    if (name, mode) in RefModeParam:
        RefModeParam[(name, mode)] = value

def get_refmodeparam(name, mode):
    return RefModeParam.get((name, mode))

def set_refcondmodeparam(name, cond, mode, value):
    if (name, cond, mode) in RefCondModeParam:
        RefCondModeParam[(name, cond, mode)] = value

def get_refcondmodeparam(name, cond, mode):
    return RefCondModeParam.get((name, cond, mode))