# -*- coding: utf-8 -*-
import ConfigParser
import json
import urllib2

class LoginAPI:
    def __init__(self,server,user,password):
        self.__url = server
        self.__user = user
        self.__password = password
        self.__header = {"Content-Type": "application/json-rpc"}
        self.__token_id = self.UserLogin()


    #登陆获取token
    def UserLogin(self):
        data = {
                "username": self.__user,
                "password": self.__password
        }
        return self.PostRequest(data)
    #推送请求
    def PostRequest(self, data):
        request = urllib2.Request(self.__url,json.dumps(data),self.__header)
        result = urllib2.urlopen(request)
        response = json.loads(result.read())
        try:
            return response['authorization']
        except KeyError:
            raise KeyError

if __name__ == '__main__':
    login = LoginAPI('http://127.0.0.1:5001/api/login','admin','kbsonlong')