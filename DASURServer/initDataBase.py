#coding=utf-8
#!/usr/bin/env python
'''
Created on 2016年8月5日

@author: sanhe
'''

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from smartclass.models import *
from datetime import datetime
from decimal import Decimal
from readconf import getSqlUrl, period_var

engine = create_engine(getSqlUrl(),echo=True)
DBSession = sessionmaker(bind=engine)


    
def ReadAndWriteTables():
    dbsession = DBSession()
    #read ipcinfo.txt
    file_obj = open('ipcinfo.txt','rb')
    try:
        list_of_all_lines = file_obj.readlines()
        for line in list_of_all_lines:
            strs = line.split(',')
            if len(strs) == 7:
                name = strs[0].strip()
                cname = strs[1].strip()
                ip = strs[2].strip()
                rtsp_type = strs[3].strip()
                fps = int(strs[4].strip())
                resolution = strs[5].strip()
                streamsize = int(strs[6].strip())
                state = False
                updatetime = datetime.now()
                dbsession.add(IPCInfo(name,cname,ip,rtsp_type,fps,resolution,streamsize,state,updatetime))
            else:
                print "ipcinfo error data: ", line
        dbsession.commit()
    finally:
        file_obj.close()
    #read areainfo.txt
    file_obj = open('areainfo.txt','rb')
    try:
        list_of_all_lines = file_obj.readlines()
        for line in list_of_all_lines:
            strs = line.split(',')
            if len(strs) == 2:
                a_id = int(strs[0].strip())
                name = strs[1].strip()
                dbsession.add(AreaInfo(a_id,name))
            else:
                print "areainfo error data: ", line
        dbsession.commit()
    finally:
        file_obj.close()
    #read refparaminfo.txt
    file_obj = open('refparaminfo.txt','rb')
    try:
        list_of_all_lines = file_obj.readlines()
        for line in list_of_all_lines:
            strs = line.split(',')
            if len(strs) == 3:
                name = strs[0].strip()
                cname = strs[1].strip()
                value = Decimal(strs[2].strip())
                updatetime = datetime.now()
                dbsession.add(RefParamInfo(name,cname,value,updatetime))
            else:
                print "refparaminfo error data: ", line
        dbsession.commit()
    finally:
        file_obj.close()
    #read refmodeparaminfo.txt
    file_obj = open('refmodeparaminfo.txt','rb')
    try:
        list_of_all_lines = file_obj.readlines()
        for line in list_of_all_lines:
            strs = line.split(',')
            if len(strs) == 4:
                name = strs[0].strip()
                mode = int(strs[1].strip())
                cname = strs[2].strip()
                value = Decimal(strs[3].strip())
                updatetime = datetime.now()
                dbsession.add(RefModeParamInfo(name,mode,cname,value,updatetime))
            else:
                print "refmodeparaminfo error data: ", line
        dbsession.commit()
    finally:
        file_obj.close()
    #read refcondmodeparaminfo.txt
    file_obj = open('refcondmodeparaminfo.txt','rb')
    try:
        list_of_all_lines = file_obj.readlines()
        for line in list_of_all_lines:
            strs = line.split(',')
            if len(strs) == 5:
                name = strs[0].strip()
                cond = int(strs[1].strip())
                mode = int(strs[2].strip())
                cname = strs[3].strip()
                value = Decimal(strs[4].strip())
                updatetime = datetime.now()
                dbsession.add(RefCondModeParamInfo(name,cond,mode,cname,value,updatetime))
            else:
                print "refcondmodeparaminfo error data: ", line
        dbsession.commit()
    finally:
        file_obj.close()
    #read logicinfo.txt
    file_obj = open('logicinfo.txt','rb')
    try:
        list_of_all_lines = file_obj.readlines()
        for line in list_of_all_lines:
            strl = line.strip()
            if strl != "":
                name = strl
                dbsession.add(LogicInfo(name,True,datetime.now()))
            else:
                print "logicinfo error data: ", line
        dbsession.commit()
    finally:
        file_obj.close()
    file_obj1 = open('serverinfo.txt','rb')
    file_obj2 = open('mepdataconstraintconf.txt','rb')
    servers = []
    try:
        list_of_all_lines = file_obj1.readlines()
        for line in list_of_all_lines:
            strl = line.strip()
            strs = line.split(',')
            if len(strs) == 6:
                name = strs[0].strip()
                cname = strs[1].strip()
                s_type = strs[2].strip()
                ip = strs[3].strip()
                ipc_name = strs[4].strip()
                pri = strs[5].strip()
                dbsession.add(ServerInfo(name,cname,s_type,ip,ipc_name,pri,False,datetime.now(),datetime.now()))
                servers.append((name,cname))
            else:
                print "serverinfo error data: ", line
        dbsession.commit()
        list_of_all_lines = file_obj2.readlines()
        for line in list_of_all_lines:
            strl = line.strip()
            strs = line.split(',')
            if len(strs) == 6:
                name = strs[0].strip()
                cname = strs[1].strip()
                min_variation = Decimal(strs[2].strip())
                min_val = Decimal(strs[3].strip())
                max_val = Decimal(strs[4].strip())
                dis_interval = int(strs[5].strip())
                dbsession.add(MEPDataConstraintConf(name,cname,min_variation,min_val,max_val,dis_interval,datetime.now()))
                #attribute 3 mep数据
                for server in servers:
                    dbsession.add(DataInfo(server[0]+ '_'+ name,server[1]+cname,None,False,None,False,None,0,min_variation,
                                           min_val,max_val,dis_interval,3,0,0,0,datetime.now()))
                    dbsession.add(ReasonDataInfo(server[0]+name,None,None,None,None,None,None))
                    dbsession.add(MepDataType(server[0]+ '_'+ name,name,server[0]))
            else:
                print "mepdataconstraintconf error data: ", line
        dbsession.commit()
    finally:
        file_obj.close()
    #read ipcvideoservermap.txt
    file_obj = open('ipcvideoservermap.txt','rb')
    try:
        list_of_all_lines = file_obj.readlines()
        for line in list_of_all_lines:
            strs = line.split(',')
            if len(strs) == 2:
                ipc_name = strs[0].strip()
                sever_name = strs[1].strip()
                dbsession.add(IPCVideoServerMap(ipc_name,sever_name))
            else:
                print "ipcvideoservermap error data: ", line
        dbsession.commit()
    finally:
        file_obj.close()
    #read nodeunitmap.txt
    file_obj = open('nodeunitmap.txt','rb')
    try:
        list_of_all_lines = file_obj.readlines()
        for line in list_of_all_lines:
            strs = line.split(',')
            if len(strs) == 2:
                node_name = strs[0].strip()
                unit_name = strs[1].strip()
                dbsession.add(NodeUnitMap(node_name,unit_name))
            else:
                print "nodeunitmap error data: ", line
        dbsession.commit()
    finally:
        file_obj.close()
    #read sessioninfo.txt
    file_obj = open('sessioninfo.txt','rb')
    try:
        list_of_all_lines = file_obj.readlines()
        for line in list_of_all_lines:
            strs = line.split(',')
            if len(strs) == 7:
                name = strs[0].strip()
                cname = strs[1].strip()
                s_type = strs[2].strip()
                s_id = int(strs[3].strip())
                server_name = strs[4].strip()
                ipc_name = strs[5].strip()
                pri = int(strs[6].strip())
                dbsession.add(SessionInfo(name,cname,s_type,s_id,server_name,ipc_name,pri,False,datetime.now()))
                #attribute 4 period数据
                dbsession.add(DataInfo(name+'_period',server[1]+'周期',None,False,None,False,None,0,Decimal(period_var),
                                           0,0,0,4,0,0,0,datetime.now()))
                dbsession.add(PeriodDataType(name+'_period',name))
                dbsession.add(ReasonDataInfo(name+'_period',None,None,None,None,None,None))
            else:
                print "sessioninfo error data: ", line
        dbsession.commit()
    finally:
        file_obj.close()
    #read datainfo.txt
    file_obj = open('datainfo.txt','rb')
    try:
        list_of_all_lines = file_obj.readlines()
        for line in list_of_all_lines:
            strs = line.split(',')
            if len(strs) == 19:
                name = strs[0].strip()
                cname = strs[1].strip()
                value = Decimal(strs[2].strip())
                error_flag = bool(strs[3].strip())
                dis_flag = bool(strs[4].strip())
                min_variation = Decimal(strs[5].strip())
                min_val = Decimal(strs[6].strip())
                max_val = Decimal(strs[7].strip())
                dis_interval = int(strs[8].strip())
                attribute = int(strs[9].strip())
                pri = int(strs[10].strip())
                start_sec = int(strs[11].strip())
                end_sec = int(strs[12].strip())
                dev_name = strs[13].strip()
                conf_name = strs[14].strip()
                link_flag = bool(strs[15].strip())
                algorithm = int(str[16].strip())
                u_type = strs[17].strip()
                server_name = strs[18].strip()
                dbsession.add(DataInfo(name,cname,value,error_flag,None,dis_flag,None,0,min_variation,min_val,
                                       max_val,dis_interval,attribute,pri,start_sec,end_sec,datetime.now()))
                dbsession.add(ReasonDataInfo(name,None,None,None,None,None,None))
                #attribute 1 dev数据
                if attribute == 1:
                    dbsession.add(DevDataType(name,dev_name,conf_name,link_flag,algorithm))
                #attribute 2 udev数据
                elif attribute == 2:
                    dbsession.add(UDevDataType(name,u_type,server_name))
            else:
                print "datainfo error data: ", line
        dbsession.commit()
    finally:
        file_obj.close()
    #read datalogicinfo.txt
    file_obj = open('datalogicinfo.txt','rb')
    try:
        list_of_all_lines = file_obj.readlines()
        for line in list_of_all_lines:
            strs = line.split(',')
            if len(strs) == 8:
                data_name = strs[0].strip()
                logic_name = strs[1].strip()
                server_name = strs[2].strip()
                data_cha = strs[3].strip()
                data_onoff = bool(strs[4].strip())
                logic_cha = strs[5].strip()
                logic_onoff = bool(strs[6].strip())
                dl_alg = Decimal(strs[7].strip())
                dbsession.add(DataLogicInfo(data_name,logic_name,server_name,data_cha,data_onoff,
                                            logic_cha,logic_onoff,dl_alg,datetime.now()))
            else:
                print "datalogicinfo error data: ", line
        dbsession.commit()
    finally:
        file_obj.close()
    #read dataipcinfo.txt
    file_obj = open('dataipcinfo.txt','rb')
    try:
        list_of_all_lines = file_obj.readlines()
        for line in list_of_all_lines:
            strs = line.split(',')
            if len(strs) == 2:
                data_name = strs[0].strip()
                ipc_name = strs[1].strip()
                dbsession.add(DataIPCInfo(data_name,ipc_name,datetime.now()))
            else:
                print "dataipcinfo error data: ", line
        dbsession.commit()
    finally:
        file_obj.close()
    #read cumulativedata.txt
    file_obj = open('cumulativedata.txt','rb')
    try:
        list_of_all_lines = file_obj.readlines()
        for line in list_of_all_lines:
            strs = line.split(',')
            if len(strs) == 2:
                data_name = strs[0].strip()
                server_name = strs[1].strip()
                dbsession.add(CumulativeData(data_name,server_name))
            else:
                print "cumulativedata error data: ", line
        dbsession.commit()
    finally:
        file_obj.close()
    #read transmitdata.txt
    file_obj = open('transmitdata.txt','rb')
    try:
        list_of_all_lines = file_obj.readlines()
        for line in list_of_all_lines:
            strs = line.split(',')
            if len(strs) == 2:
                data_name = strs[0].strip()
                server_name = strs[1].strip()
                dbsession.add(TransmitData(data_name,server_name))
            else:
                print "transmitdata error data: ", line
        dbsession.commit()
    finally:
        file_obj.close()
if __name__ == "__main__":
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    dbsession = DBSession()
    dbsession.add(ServerInfo('server1','区域服务器','region','172.16.1.15',None,0,False,datetime.now(),datetime.now()))
    dbsession.commit()
#     ReadAndWriteTables()