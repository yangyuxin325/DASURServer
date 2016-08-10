#coding=utf-8
#!/usr/bin/env python
'''
Created on 2016年7月4日

@author: sanhe
'''
import fcntl
import socket
import struct
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from readconf import getRemoteUrl
from smartclass.models import RefParamInfo, RefModeParamInfo, RefCondModeParamInfo, ServerInfo
from logset.util import def_refparam, def_refmodeparam, def_refcondmodeparam
from smartserver.serverfactory import CreateServer

def get_ip_address( ifname):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    return socket.inet_ntoa(fcntl.ioctl(
                                        sock.fileno(),
                                        0x8915,  # SIOCGIFADDR
                                        struct.pack('256s', ifname[:15])
                                        )[20:24])

class DSAURServer(object):
    instance = None
    def __new__(cls, *args, **kwarg):
        if not cls.instance:
            cls.instance = super(DSAURServer, cls).__new__(cls, *args, **kwarg)
        return cls.instance
    
    def Init(self):
        self.Start = False
        server_ip = get_ip_address('eth0')
        engine = create_engine(getRemoteUrl(server_ip),echo=True)
        DBSession = sessionmaker(bind=engine)
        dbsesson = DBSession()
        for data in dbsesson.query(RefParamInfo).all():
            def_refparam(data.name, data.value)
        for data in dbsesson.query(RefModeParamInfo).all():
            def_refmodeparam(data.name, data.mode, data.value)
        for data in dbsesson.query(RefCondModeParamInfo).all():
            def_refcondmodeparam(data.name, data.cond, data.mode, data.value)
        serverinfo = dbsesson.query(ServerInfo).filter_by(ip=server_ip).one_or_none()
        if serverinfo is None:
            return
        CreateServer(dbsesson, serverinfo.type)
        rserverinfo = dbsesson.query(ServerInfo).filter_by(type = 'region').one_or_none()
        smartclass.data_server.rserverinfo = rserverinfo