#coding=utf-8
#!/usr/bin/env python
'''
Created on 2016年8月9日

@author: sanhe
'''

from sqlalchemy import Column, String, Integer, Boolean, DECIMAL ,TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

__all__ = ['Base','IPCInfo','ServerInfo','NodeUnitMap','IPCVideoServerMap','SessionInfo','AreaInfo','DeviceInfo',
           'MEPDataConstraintConf','DataInfo','ReasonDataInfo','DevDataLink','DevDataType','UDevDataType',
           'PeriodDataType','MepDataType','LogicInfo','DataLogicInfo','DataLogicStorage','DataIPCInfo',
           'CumulativeData','TransmitData','SerialSearch','RefParamInfo','RefModeParamInfo',
           'RefModeParamInfo','RefCondModeParamInfo','DataHistory']

Base = declarative_base()

class IPCInfo(Base):
    __tablename__ = 'ipcinfo'
    name = Column(String(30), primary_key=True)
    cname = Column(String(30), unique=True)
    ip = Column(String(20), nullable=False, unique=True)
    rtsp_type = Column(String(30))
    fps = Column(Integer, nullable=False)
    resolution = Column(String(12), nullable=False)
    streamsize = Column(Integer, nullable=False)
    state = Column(Boolean, nullable=False)
    updatetime = Column(TIMESTAMP)
    
    def __init__(self, name, cname, ip, url, fps, resolution, streamsize, state, updatetime):
        self.name = name
        self.cname = cname
        self.ip = ip
        self.url = url
        self.fps = fps
        self.resolution = resolution
        self.streamsize = streamsize
        self.state = state
        self.updatetime = updatetime
        
    def __repr__(self):
        return "<IPCInfo: %r,%r,%r,%r,%r,%r,%r,%r,%r>" % (self.name,self.cname,self.ip,
                                                         self.url,self.fps,
                                                         self.resolution,
                                                         self.streamsize,
                                                         self.state,
                                                         self.updatetime)
        
class ServerInfo(Base):
    __tablename__ = 'serverinfo'
    name = Column(String(30), primary_key=True)
    cname = Column(String(30), unique=True)
    type = Column(String(10), nullable=False)
    ip = Column(String(15), nullable=False, unique=True)
    ipc_name = Column(String(30), ForeignKey('ipcinfo.name', ondelete='SET NULL', onupdate='CASCADE'))
    pri = Column(Integer,nullable=False)
    state = Column(Boolean, nullable=False)
    savedays = Column(Integer)
    updatetime = Column(TIMESTAMP)
    runtime = Column(TIMESTAMP)
    ipc = relationship('IPCInfo', backref='serverinfo', uselist=False, lazy=True)
    sessions = relationship('SessionInfo', backref='serverinfo', lazy='dynamic')
    udatatypes = relationship('UDevDataType', backref='serverinfo', lazy='dynamic')
    mdatatypes = relationship('MepDataType', backref='serverinfo', lazy='dynamic')
    node_unit = relationship('NodeUnitMap', primaryjoin='ServerInfo.name==NodeUnitMap.node_name', uselist=False, lazy=True)
    unit_nodes = relationship('NodeUnitMap', primaryjoin='ServerInfo.name==NodeUnitMap.unit_name', lazy='dynamic')
     
    def __init__(self, name, cname, s_type, ip, ipc_name, pri, state, updatetime, runtime):
        self.name = name
        self.cname = cname
        self.type = s_type
        self.ip = ip
        self.ipc_name = ipc_name
        self.pri = pri
        self.state = state
        self.updatetime = updatetime
        self.runtime = runtime
         
    def __repr__(self):
        return '<ServerInfo: %r,%r,%r,%r,%r,%r,%r,%r,%r>' % (self.name,self.cname,self.type,
                                                             self.ip,self.ipc_name,self.pri,
                                                             self.state,self.updatetime,self.runtime)
        
class NodeUnitMap(Base):
    __tablename__ = 'nodeunitmap'
    node_name = Column(String(30), ForeignKey('serverinfo.name', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    unit_name = Column(String(30), ForeignKey('serverinfo.name', ondelete='CASCADE', onupdate='CASCADE'))
    node = relationship('ServerInfo', foreign_keys=[node_name], lazy=True)
    unit = relationship('ServerInfo', foreign_keys=[unit_name], lazy=True)
    
    def __init__(self, node_name, unit_name):
        self.node_name = node_name
        self.unit_name = unit_name
        
    def __repr__(self):
        return '<NodeUnitMap: %r,%r>' % (self.node_name, self.unit_name)        
        
class IPCVideoServerMap(Base):
    __tablename__ = 'ipcvideosevermap'
    ipc_name = Column(String(30), ForeignKey('ipcinfo.name', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    server_name = Column(String(30), ForeignKey('serverinfo.name', ondelete='CASCADE', onupdate='CASCADE'))
    ipc = relationship('IPCInfo', backref = 'ipcvideosevermap', uselist=False, lazy=True)
    server = relationship('ServerInfo', backref = 'ipcvideosevermap', uselist=False, lazy=True)
    
    def __init__(self, ipc_name, server_name):
        self.ipc_name = ipc_name
        self.server_name = server_name
        
    def __repr__(self):
        return '<IPCVideoServerMap: %r,%r>' % (self.ipc_name, self.server_name)
 
class SessionInfo(Base):
    __tablename__ = 'sessioninfo'
    name = Column(String(30), primary_key=True)
    cname = Column(String(30), unique=True)
    type = Column(Integer, nullable=False)
    id = Column(Integer, nullable=False)
    server_name = Column(String(30), ForeignKey('serverinfo.name', ondelete='CASCADE', onupdate='CASCADE'))
    ipc_name = Column(String(30), ForeignKey('ipcinfo.name', ondelete='SET NULL', onupdate='CASCADE'))
    pri = Column(Integer, nullable=False)
    state = Column(Boolean, nullable=False)
    updatetime = Column(TIMESTAMP)
    ipc = relationship('IPCInfo', backref = 'sessioninfo', uselist=False, lazy=True)
    server = relationship('ServerInfo', backref = 'sessioninfo', uselist=False, lazy=True)
    devices = relationship('DeviceInfo', backref='sessioninfo', lazy='dynamic')
    pdatatype = relationship('PeriodDataType', backref='sessioninfo', uselist=False, lazy=True)
      
    def __init__(self, name, cname, s_type, s_id, server_name, ipc_name, pri, state, updatetime):
        self.name = name
        self.cname = cname
        self.type = s_type
        self.id = s_id
        self.server_name = server_name
        self.ipc_name = ipc_name
        self.pri = pri
        self.state = state
        self.updatetime = updatetime
          
    def __repr__(self):
        return '<SessionInfo  %r,%r,%r,%r,%r,%r,%r,%r,%r>' % (self.name, self.cname, self.type,
                                                              self.id, self.server_name, self.ipc_name,
                                                              self.pri, self.state, self.updatetime)
       

class AreaInfo(Base):
    __tablename__ = 'areainfo'
    id = Column(Integer, primary_key=True)
    name = Column(String(30), unique=True)
    
    def __init__(self, a_id, name):
        self.id = a_id
        self.name = name
        
    def __repr__(self):
        return '<AreaInfo %r,%r>' % (self.id, self.name)
        
class DeviceInfo(Base):
    __tablename__ = 'deviceinfo'
    name = Column(String(30), primary_key=True)
    cname = Column(String(30), unique=True)
    type = Column(String(20), nullable=False)
    id = Column(Integer, nullable=False)
    area_id = Column(Integer, ForeignKey('areainfo.id', ondelete='SET NULL', onupdate='CASCADE'))
    session_name = Column(String(30), ForeignKey('sessioninfo.name', ondelete='CASCADE', onupdate='CASCADE'))
    session = relationship('SessionInfo', backref = 'deviceinfo', uselist=False, lazy=True)
    area = relationship('AreaInfo', backref = 'areainfo', lazy=True)
    datatypes = relationship('DevDataType', backref='deviceinfo', lazy='dynamic')
    
    def __init__(self, name, cname, d_type, d_id, area_id, session_name):
        self.name = name
        self.cname = cname
        self.type = d_type
        self.id = d_id
        self.area_id = area_id
        self.session_name = session_name
        
    def __repr__(self):
        return '<DeviceInfo: %r,%r,%r,%r,%r,%r>' % (self.name, self.cname, 
                                                    self.type, self.id, 
                                                    self.area_id, self.session_name)

class MEPDataConstraintConf(Base):
    __tablename__ = 'mepdataconstraintconf'
    name = Column(String(20), primary_key=True)
    cname = Column(String(20), unique=True)
    min_variation = Column(DECIMAL(10,2), nullable=False)
    min_val = Column(DECIMAL(20,2))
    max_val = Column(DECIMAL(20,2))
    dis_interval = Column(Integer)
    addtime = Column(TIMESTAMP)
    mdatatypes = relationship('MepDataType', backref='mepdataconstraintconf', lazy='dynamic')
    
    def __init__(self, name, cname, min_variation, min_val, max_val, dis_terval, addtime):
        self.name = name
        self.cname = cname
        self.min_variation = min_variation
        self.min_val = min_val
        self.max_val = max_val
        self.dis_interval = dis_terval
        self.addtime = addtime
        
    def __repr__(self):
        return '<MEPDataConstraintConf: %r,%r,%r,%r,%r,%r>' % (self.name, self.cname, self.min_variation,
                                                               self.min_val, self.max_val,
                                                               self.dis_interval, self.addtime)
          
class DataInfo(Base):
    __tablename__ = 'datainfo'
    name = Column(String(50), primary_key=True)
    cname = Column(String(50), unique=True)
    value = Column(DECIMAL(20,2))
    error_flag = Column(Boolean)
    time = Column(TIMESTAMP)
    dis_flag = Column(Boolean)
    dis_time = Column(TIMESTAMP)
    rs_type = Column(Integer)
    min_variation = Column(DECIMAL(10,2), nullable=False)
    min_val = Column(DECIMAL(20,2))
    max_val = Column(DECIMAL(20,2))
    dis_interval = Column(Integer)
    attribute = Column(Integer)
    pri = Column(Integer, nullable=False)
    start_sec = Column(Integer)
    end_sec = Column(Integer)
    addtime = Column(TIMESTAMP)
    reason = relationship('ReasonDataInfo', backref='datainfo', primaryjoin='DataInfo.name==ReasonDataInfo.name',lazy=True, uselist=False)
    datatype = relationship('DevDataType', backref='datainfo', lazy=True, uselist=False)
    udatatype = relationship('UDevDataType', backref='datainfo', primaryjoin='DataInfo.name==UDevDataType.name', lazy=True, uselist=False)
    pdatatype = relationship('PeriodDataType', backref='datainfo', primaryjoin='DataInfo.name==PeriodDataType.name', lazy=True, uselist=False)
    mdatatype = relationship('MepDataType', backref='datainfo', primaryjoin='DataInfo.name==MepDataType.name', lazy=True, uselist=False)
    dataipcs = relationship('DataIPCInfo', backref='datainfo', lazy='dynamic')
    transdatas = relationship('TransmitData', backref='datainfo', lazy='dynamic')
    
    def __init__(self, name, cname, value, error_flag, time, dis_flag, dis_time,
                 rs_type, min_variation, min_val, max_val, dis_interval, attribute, 
                 pri, start_sec, end_sec, addtime):
        self.name = name
        self.cname = cname
        self.value = value
        self.error_flag = error_flag
        self.time = time
        self.dis_flag = dis_flag
        self.dis_time = dis_time
        self.rs_type = rs_type
        self.min_variation = min_variation
        self.min_val = min_val
        self.max_val = max_val
        self.dis_interval = dis_interval
        self.attribute = attribute
        self.pri = pri
        self.start_sec = start_sec
        self.end_sec = end_sec
        self.addtime = addtime
        
    def __repr__(self):
        return '<DataInfo: %r,%r,%r,%r,%r,%r,%r,%r,%r,%r,%r,%r,%r,%r,%r,%r,%r,%r>' % (
                self.name, self.cname, self.value, self.error_flag, self.time, self.dis_flag,self.dis_time,
                self.rs_type, self.min_variation, self.min_val, self.max_val, self.dis_interval, self.attribute,
                self.pri, self.start_sec, self.end_sec, self.characteristic, self.addtime)
        
    
class ReasonDataInfo(Base):
    __tablename__ = 'reasondatainfo'
    name = Column(String(50), ForeignKey('datainfo.name', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    rs_name = Column(String(50), ForeignKey('datainfo.name', onupdate='CASCADE'))
    rs_value = Column(DECIMAL(20,2))
    rs_change_flag = Column(Integer)
    rs_conf = Column(String(256));
    rs_user = Column(String(256));
    rs_time = Column(TIMESTAMP)
    data = relationship('DataInfo', backref='reasondatainfo', foreign_keys=[name], lazy=True)
    
    def __init__(self, name, rs_name, rs_value, rs_change_flag, rs_conf, rs_user, rs_time):
        self.name = name
        self.rs_name = rs_name
        self.rs_value = rs_value
        self.rs_change_flag = rs_change_flag
        self.rs_user = rs_user
    
    def __repr__(self):
        return '<ReasonDataInfo: %r,%r,%r,%r,%r,%r,%r>' % (self.name, self.rs_name, self.rs_value,
                                                           self.rs_change_flag, self.rs_conf,
                                                           self.rs_user, self.rs_time)
        
class DevDataLink(Base):
    __tablename__ = 'devdatalink'
    id = Column(Integer, primary_key=True, autoincrement=True)
    conf_name = Column(String(30), nullable=False)
    dev_name = Column(String(30), ForeignKey('deviceinfo.name', ondelete='CASCADE', onupdate='CASCADE'))
    link_key = Column(String(30), nullable=False)
    link_type = Column(String(30), nullable=False)
    link_para1 = Column(Integer, nullable=False)
    dev = relationship('DeviceInfo', backref='devdatalink', lazy=True)
    
    def __init__(self, conf_name, dev_name, link_key, link_type, link_para1):
        self.conf_name = conf_name
        self.dev_name = dev_name
        self.link_key = link_key
        self.link_type = link_type
        self.link_para1 = link_para1
        
    def __repr__(self):
        return '<DevDataLink: %r,%r,%r,%r,%r>' % (self.conf_name, self.dev_name, self.link_key,
                                                     self.link_type, self.link_para1)
    
class DevDataType(Base):
    __tablename__ = 'devdatatype'
    name = Column(String(50), ForeignKey('datainfo.name', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    dev_name = Column(String(30), ForeignKey('deviceinfo.name', ondelete='CASCADE', onupdate='CASCADE'))
    conf_name = Column(String(30), nullable=False)
    link_flag = Column(Boolean)
    algorithm = Column(Integer)
    dev = relationship('DeviceInfo', backref='devdatatype', lazy=True)
    data = relationship("DataInfo", backref='devdatatype', lazy=True)
    
    def __init__(self, name, dev_name, conf_name, link_flag, algorithm):
        self.name = name
        self.dev_name = dev_name
        self.conf_name = conf_name
        self.link_flag = link_flag
        self.algorithm = algorithm
        
    def __repr__(self):
        return '<DevDataType: %r,%r,%r,%r,%r>' % (self.name, self.dev_name, self.conf_name, self.link_flag, self.algorithm)
   
class UDevDataType(Base):
    __tablename__ = 'udevdatatype'
    name = Column(String(50), ForeignKey('datainfo.name', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    type = Column(String(30), nullable=False)
    server_name = Column(String(30), ForeignKey('serverinfo.name', ondelete='CASCADE', onupdate='CASCADE'))
    data = relationship("DataInfo", backref='udevdatatype', lazy=True)
    server = relationship('ServerInfo', backref ='udevdatatype', lazy=True)
    
    def __init__(self, name, u_type, server_name):
        self.name = name
        self.type = u_type
        self.server_name = server_name
        
    def __repr__(self):
        return '<UDevDataType: %r,%r,%r>' % (self.name, self.type, self.server_name)
    
class PeriodDataType(Base):
    __tablename__ = 'periodatatype'
    name = Column(String(50), ForeignKey('datainfo.name', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    session_name = Column(String(30), ForeignKey('sessioninfo.name', ondelete='CASCADE', onupdate='CASCADE'))
    data = relationship("DataInfo", backref='periodatatype', lazy=True)
    session = relationship('SessionInfo', backref='periodatatype', lazy=True)
    
    def __init__(self, name, session_name):
        self.name = name
        self.session_name = session_name
        
    def __repr__(self):
        return '<PeriodDataType: %r,%r>' % (self.name, self.session_name)
    
class MepDataType(Base):
    __tablename__ = 'mepdatatype'
    name = Column(String(50), ForeignKey('datainfo.name', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    mep_name = Column(String(20), ForeignKey('mepdataconstraintconf.name'), nullable=False)
    server_name = Column(String(30), ForeignKey('serverinfo.name', ondelete='CASCADE', onupdate='CASCADE'))
    data = relationship("DataInfo", backref='mepdatatype', lazy=True)
    mepconstraint = relationship("MEPDataConstraintConf", backref='mepdatatype', lazy=True)
    server = relationship('ServerInfo', backref ='mepdatatype', lazy=True)
    
    def __init__(self, name, mep_name, server_name):
        self.name = name
        self.mep_name = mep_name
        self.server_name = server_name
        
    def __repr__(self):
        return '<MepDataType: %r,%r,%r>' % (self.name, self.mep_name, self.server_name)

class LogicInfo(Base):
    __tablename__ = 'logicinfo'
    name = Column(String(50), primary_key=True)
    status = Column(Boolean, nullable=False)
    addtime = Column(TIMESTAMP)
    
    def __init__(self, name, status, addtime):
        self.name = name
        self.status = status
        self.addtime = addtime
        
    def __repr__(self):
        return '<LogicInfo: %r,%r,%r>' % (self.name, self.status, self.addtime)
    
class DataLogicInfo(Base):
    __tablename__ = 'datalogicinfo'
    id = Column(Integer, primary_key=True, autoincrement=True)
    data_name = Column(String(50), ForeignKey('datainfo.name'))
    logic_name = Column(String(50), ForeignKey('logicinfo.name'))
    server_name = Column(String(30), ForeignKey('serverinfo.name'))
    data_cha = Column(String(50))
    data_onoff = Column(Boolean, nullable=False)
    logic_cha = Column(String(50))
    logic_onoff = Column(Boolean, nullable=False)
    dl_alg = Column(DECIMAL(20,2))
    addtime = Column(TIMESTAMP)
    data = relationship("DataInfo", backref='datalogicinfo', lazy=True)
    logic = relationship("LogicInfo", backref='datalogicinfo', lazy=True)
    server = relationship("ServerInfo", backref='datalogicinfo', lazy=True)
    
    def __init__(self, data_name, logic_name, server_name, data_cha, data_onoff, logic_cha, logic_onoff, dl_alg, addtime):
        self.data_name = data_name
        self.logic_name = logic_name
        self.server_name = server_name
        self.data_cha = data_cha
        self.data_onoff = data_onoff
        self.logic_cha = logic_cha
        self.logic_onoff = logic_onoff
        self.dl_alg = dl_alg
        self.addtime = addtime
        
    def __repr__(self):
        return '<DataLogicInfo: %r,%r,%r,%r,%r,%r,%r,%r,%r>' % (self.data_name, self.logic_name, self.server_name,self.data_cha,
                                                    self.data_onoff, self.logic_cha, self.logic_onoff, self.dl_alg, self.addtime)
        
class DataLogicStorage(Base):
    __tablename__ = 'datalogicstorage'
    id = Column(Integer, primary_key=True, autoincrement=True)
    data_name = Column(String(50), ForeignKey('datainfo.name'))
    logic_name = Column(String(50), ForeignKey('logicinfo.name'))
    logic_charc = Column(String(50))
    status = Column(Boolean, nullable=False)
    runtime = Column(TIMESTAMP)
    data = relationship("DataInfo", backref='datalogicstorage', lazy=True)
    logic = relationship("LogicInfo", backref='datalogicstorage', lazy=True)
    
    def __init__(self, data_name, logic_name, server_name, logic_charc, status ,runtime):
        self.data_name = data_name
        self.logic_name = logic_name
        self.server_name = server_name
        self.logic_charc = logic_charc
        self.status = status
        self.runtime = runtime
        
    def __repr__(self):
        return '<DataLogicInfo: %r,%r,%r,%r,%r>' % (self.data_name, self.logic_name, self.server_name,
                                                    self.logic_charc, self.runtime)

class DataIPCInfo(Base):
    __tablename__ = 'dataipcinfo'
    data_name = Column(String(50), ForeignKey('datainfo.name'), primary_key=True)
    ipc_name = Column(String(30), ForeignKey('ipcinfo.name'), primary_key=True)
    addtime = Column(TIMESTAMP)
    data = relationship("DataInfo", backref='dataipcinfo', lazy=True)
    ipc = relationship("IPCInfo", backref='dataipcinfo', lazy=True)
    
    def __init__(self, data_name, ipc_name, addtime):
        self.data_name = data_name
        self.ipc_name = ipc_name
        self.addtime = addtime
    
    def __repr__(self):
        return '<DataIPCInfo: %r,%r,%r>' % (self.data_name, self.ipc_name, self.addtime)
    
class CumulativeData(Base):
    __tablename__ = 'cumulativedata'
    data_name = Column(String(50), ForeignKey('datainfo.name'), primary_key=True)
    server_name = Column(String(30), ForeignKey('serverinfo.name'))
    
    def __init__(self, data_name, server_name):
        self.data_name = data_name
        self.server_name = server_name
        
    def __repr__(self):
        return '<CumulativeData: %r,%r>' % (self.data_name, self.server_name)
    
class TransmitData(Base):
    __tablename__ = 'transmitdata'
    data_name = Column(String(50), ForeignKey('datainfo.name'), primary_key=True)
    server_name = Column(String(30), ForeignKey('serverinfo.name'), primary_key=True)
    data = relationship("DataInfo", backref='transmitdata', lazy=True)
    server = relationship("ServerInfo", backref='transmitdata', lazy=True)
    
    def __init__(self, data_name, server_name):
        self.data_name = data_name
        self.server_name = server_name
        
    def __repr__(self):
        return '<TransmitData: %r,%r>' % (self.data_name, self.server_name)
    
class SerialSearch(Base):
    __tablename__ = 'serialsearch'
    index_name = Column(String(20), primary_key=True)
    value = Column(Integer)
    
    def __init__(self, index_name, value):
        self.index_name = index_name
        self.value = value
    
    def __repr__(self):
        return '<SerialSearch: %r,%r>' % (self.index_name, self.value)
    
class RefParamInfo(Base):
    __tablename__ = 'refparaminfo'
    name = Column(String(30), primary_key=True)
    cname = Column(String(30), unique=True)
    value = Column(DECIMAL(20,2))
    updatetime = Column(TIMESTAMP)
    
    def __init__(self, name, cname, value, updatetime):
        self.name = name
        self.cname = cname
        self.value = value
        self.updatetime = updatetime
        
    def __repr__(self):
        return '<RefParamInfo: %r,%r,%r,%r>' % (self.name, self.cname, self.value, self.updatetime)
    
class RefModeParamInfo(Base):
    __tablename__ = 'refmodeparaminfo'
    name = Column(String(30), primary_key=True)
    mode = Column(Integer, primary_key=True, autoincrement=False)
    cname = Column(String(30))
    value = Column(DECIMAL(20,2))
    updatetime = Column(TIMESTAMP)
    
    def __init__(self, name, mode ,cname, value, updatetime):
        self.name = name
        self.mode = mode
        self.cname = cname
        self.value = value
        self.updatetime = updatetime
        
    def __repr__(self):
        return '<RefModeParamInfo: %r,%r,%r,%r,%r>' % (self.name, self.mode, self.cname, self.value, self.updatetime)
 
class RefCondModeParamInfo(Base):
    __tablename__ = 'refcondmodeparaminfo'
    name = Column(String(30), primary_key=True)
    cond = Column(Integer, primary_key=True, autoincrement=False)
    mode = Column(Integer, primary_key=True, autoincrement=False)
    cname = Column(String(30))
    value = Column(DECIMAL(20,2))
    updatetime = Column(TIMESTAMP)
     
    def __init__(self, name, cond ,mode ,cname, value, updatetime):
        self.name = name
        self.cond = cond
        self.mode = mode
        self.cname = cname
        self.value = value
        self.updatetime = updatetime
         
    def __repr__(self):
        return '<RefCondModeParamInfo: %r,%r,%r,%r,%r,%r>' % (self.name, self.cond, self.mode, self.cname, self.value, self.updatetime)

class DataHistory(Base):
    __tablename__ = 'datahistory'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    change_flag = Column(Integer, nullable=True)
    value = Column(DECIMAL(20,2), nullable=True)
    error_flag = Column(Boolean, nullable=True)
    time = Column(TIMESTAMP, nullable=True)
    dis_flag = Column(Boolean, nullable=True)
    dis_time = Column(TIMESTAMP, nullable=True)
    rs_type = Column(Integer)
    rs_name = Column(String(50))
    rs_value = Column(DECIMAL(20,2))
    rs_change_flag = Column(Integer)
    rs_conf = Column(String(256));
    rs_user = Column(String(256));
    rs_time = Column(TIMESTAMP)
    addtime = Column(TIMESTAMP)