#coding:utf8
from zabbix_client import ZabbixServerProxy
from api import app


class Zabbix():
    def __init__(self,data):
        self.zb = ZabbixServerProxy(data['zabbix_url'])
        self.zb.user.login(user=data['zabbix_user'], password=data['zabbix_password'])
    
    def get_hosts(self):
        return self.zb.host.get(output=['hostid','host'])

    def get_host_tem(self):
        data = {
           "output": ["hostid","name"],
           "selectParentTemplates": ["templateid","name"]
          }
        ret = self.zb.host.get(**data)
        return ret

    def get_interface(self, hostids):
        data = self.zb.hostinterface.get(hostids=hostids, output=['hostid','ip'])
        ret = {}
        for d in data:
            ret[d['hostid']] = d['ip']
        return ret
    def get_hostgroup(self):
        return self.zb.hostgroup.get(output=['groupid','name'])

    def create_host(self, params):
        return self.zb.host.create(**params) 

    def get_template(self): 
        ret =  self.zb.template.get(output=["templateid","name"])
        return  ret

    def link_template(self, hostid, templateids):
        data = {
                "hostid":hostid,
                "templates":templateids
              } 
        ret=self.zb.host.update(data)
        return ret
        
    
    def unlink_template(self, hostid, templateid):
        return self.zb.host.update(hostid=hostid, templates_clear = [{"templateid":templateid}])

    def create_maintenance(self, params):
        return self.zb.maintenance.create(**params)

    def get_maintenance(self):
        data = {
            "output": "extend",
            "selectHosts": ["name"] 
        }
        ret = self.zb.maintenance.get(**data)
        return ret

    def del_maintenance(self, maintenanceids):
        return self.zb.maintenance.delete(maintenanceids)

    def get_trigger(self, params):
        return self.zb.trigger.get(**params)

    def get_alerts(self, params):
        return self.zb.alert.get(**params)

    def host_status(self, hostid, status):
        return self.zb.host.update(hostid=hostid, status = status)

    def hostid_get_template(self,hostids):
        data = {
           "output": ["hostid"],
           "selectParentTemplates": ["templateid"],
           "hostids": hostids
          }

        return self.zb.host.get(**data)
  
    def get_graphid(self,hostid):
        data = {
                "selectGraphs": ["graphid","name"],
                "filter": {"hostid": hostid}
                }

        ret = self.zb.host.get(**data)
        return ret[0]['graphs']




zabbix_server='http://www.along.party:8000'
zabbix_user='Admin'
zabbix_pass='zabbix'
from zabbix_api import ZabbixAPI
zapi = ZabbixAPI(zabbix_server)
zapi.login('Admin','zabbix')
host_name = 'Zabbix-docker'
print zapi.host.get({"filter":{"host":host_name}})[0]['name']



##参考zabbix官网api文档https://www.zabbix.com/documentation/3.4/zh/api/reference
from pyzabbix import ZabbixAPI

zapi = ZabbixAPI(zabbix_server)
zapi.login(zabbix_user, zabbix_pass)
print("Connected to Zabbix API Version %s" % zapi.api_version())

##监控图表
# for graph in zapi.graph.get(output="extend",hostids=10084):
#     print graph
#
# ##监控主机
for h in zapi.host.get(output="extend"):
    print(h['hostid'])
#
# #监控项
# for item in zapi.item.get(output="extend",hostids=10084):
#     print item

#主机组
for group in zapi.hostgroup.get(output="extend"):
    print group['groupid'],group['name']


host = 'Linux server'
#创建主机
def hostcreate(host,ip,group,port=10050):
    data = {
            "host": host,
            "interfaces": [
                {
                    "type": 1,
                    "main": 1,
                    "useip": 1,
                    "ip": ip,
                    "dns": "",
                    "port": port
                }
              ],
            "groups": [
                {
                    "groupid": int(group)
                }
             ]
             }
    ret = zapi.host.create(data)
    return ret


#添加主机模板
def hostupdate(hostid,data):
    up_data = {
            "hostid" : hostid,
            data.keys()[0] : data.values()[0]
        }
    return zapi.host.update(up_data)

data = {"templates_clear": [
            {
                "templateid": "10093"
            }
        ]}

print hostupdate(10254,data)