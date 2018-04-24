# -*- coding: utf-8 -*-
from flask import render_template
from ZabbixAPI import ZabbixAPI
from api import app,jsonrpc
from auth import auth_login
from utils import write_log

import ConfigParser
import time,json,traceback

@app.route('/api/zbhost')
# @auth_login
def host(**kwargs):
    try:
        zapi=ZabbixAPI()
        host_list=zapi.HostGet()
        group_list=zapi.HostGroupGet()
        template_list=zapi.TemplateGet()
        write_log('api').info("create zabbix host  scucess" )
        return json.dumps({'code': 0,'result': {'hosts':host_list,'groups':group_list,'templates':template_list}})
    except Exception as e:
        error=str(e)
        write_log('api').error("create zabbix host error: %s" % traceback.format_exc())
        return json.dumps({'code': 1, 'errmsg': 'create zabbix host fail \n %s ' % error})



@app.route('/api/zbhost_create')
@auth_login
def host_create(request):
    name=request.GET.get('name','')
    ip=request.GET.get('ip','')
    groupid=request.GET.get('groupid','')
    templateid=request.GET.get('templateid','')
    try:
        zapi=ZabbixAPI()
        hostcreate=zapi.HostCreate(name,ip,groupid,templateid)
        if hostcreate['hostids']:
            result=u"主机%s创建成功，ID为%s."%(name,hostcreate['hostids'])
        else:
            result=u"主机%s创建失败."%(name)
    except Exception as e:
        result=str(e)
    return JsonResponse(result,safe=False)


@app.route('/api/zbhost_create')
@auth_login
def template(request):

    return render_template(request, 'ZABBIX/template.html', locals())

@app.route('/api/zbhost_create')
@auth_login
def item(request):
    cf = ConfigParser.ConfigParser()
    cf.read("SaltRuler/config.ini")
    itemurl = cf.get("zabbix_server","itemurl")

    hostid=request.GET.get('hostid','')
    try:
        zapi=ZabbixAPI()
        host_list=zapi.HostGet()
        if hostid:
            item_list=zapi.ItemGet(hostid=hostid)
        else:
            item_list=zapi.ItemGet()
        #时间戳转化成日期格式
        for item in item_list:
            item['lastclock']= time.strftime('%Y/%m/%d %H:%M', time.localtime(float(item['lastclock'])))
    except Exception as e:
        error=str(e)
    return render_template(request, 'ZABBIX/item.html', locals())

@app.route('/api/zbhost_create')
@auth_login
def graph(request):
    cf = ConfigParser.ConfigParser()
    cf.read("SaltRuler/config.ini")
    graphurl = cf.get("zabbix_server","graphurl")

    hostid=request.GET.get('hostid','')
    try:
        zapi=ZabbixAPI()
        host_list=zapi.HostGet()
        if hostid:
            graph_list=zapi.GraphGet(hostid=hostid)
        # else:
        #     graph_list=zapi.GraphGet()
    except Exception as e:
        error=str(e)
    return render_template(request, 'ZABBIX/graph.html', locals())


@app.route('/api/zbhost_create')
@auth_login
def screen(request):
    return render_template(request, 'ZABBIX/screen.html', locals())

@app.route('/api/zbhost_create')
@auth_login
def history(request):
    itemid=request.GET.get('itemid','')
    data_type=request.GET.get('data_type','0')
    try:
        zapi=ZabbixAPI()
        if itemid:
            value=[]
            clock=[]
            item=zapi.ItemGet(itemid=itemid)[0]
            host=zapi.HostGet(hostid=item['hostid'])[0]
            history_list=zapi.History(itemid,int(data_type))
            print zapi.History(itemid=29112,data_type=0)
            print history_list
            for history in history_list:
                print history
                value.append(float(history['value']))
                clock.append(time.strftime('%Y/%m/%d %H:%M', time.localtime(float(history['clock']))))
            print history_list
    except Exception as e:
        error=str(e)
    return render_template(request, 'ZABBIX/history.html', locals())

