#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import enum
from base64 import b64decode
from base64 import b64encode
from Crypto.PublicKey import RSA
import requests
import random
import string
import re
from faker import Faker
from faker.providers import internet
import socket

fake = Faker()
fake.add_provider(internet)

VULNS = "2:1" 
PORT = '3377'

def id_generator(size=8, chars= string.digits + string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))

def genflag():
    chars= string.digits + string.ascii_uppercase
    strr = ''.join(random.choice(chars) for _ in range(31))
    return strr + '='

def getPromocode(resp):
    regex = r'promocode:<br\/><b>\[(.*?)\]<\/b><\/p>'
    token = re.findall(regex, resp)[0]
    PRIVKEY = RSA.importKey(b'0\x82\x04\xa4\x02\x01\x00\x02\x82\x01\x01\x00\xaa\x08\xac\x83kx\xec\xfd\xc0Iol\xa3Y\xd6\xba\x85n7\x08\xef<\x01\xa1 \xce5.\xa1\x9a<t\xf3Z\x88\x18\xaf\xf9\x05\xb1\xa9\x14J\xaaB\xf1\xc5&LN\x94\x1c\xec\x0e:\x80\xf0?\x1d\x98Ih_\x1c\x1b\x1f\xbbY\x91\xbaA\xe5\x08\xbcL,f\xe28>\x0c\xf9\x83\xc6\xb8Us\xc9~}n\xe7c\x94#\xf4\xa7G\xd7F2h\rn\x1cO\x1a\tv\x03rW\xaa\x07\xad@:\xc4%\x1c\xb9Ec~\xe9\xde&\xed\x86\\KL\xb0\xe3\xac\xd8\xfddgG\xe4\xec,\xb4\xef\x0b\x11\x81\xe1\xb4l;\xf1\xdeH\xf6!\x9c\x03\xf2\xa4\xb0\xc0\xbf\n\xc7\xc4\x99\t\xdbW\xa4\\!\xab\xc3_\x14Y\x05\xc1h,\xac35\x16\xc0\xb2\xf9\xdd\x15\x1e\xb0\x14\xc1\x0b^\xf1\xf8\x03\xbb\xf72\x1b\xcf,I|\xfdq\x8cg@\xbd\xee\x05\xb5}\xfa\xd7\xc7\xb4\x85\\1>\xce+\xfd\xc4\x8f\xcc\xba\xb1\x12hj\xf1\x1b\xb7\xc0\xf1\x04\xc6\xfc\x8e]?\'X\xe4\x89F\xad\xb7\x02\x03\x01\x00\x01\x02\x82\x01\x01\x00\x9f\xf8\xf7-\xd2\x00|\xa0$\xb82\x8f\xf8\x83\xfe\xa5\x90\x01\xe8\xdf\x8c\r]\xcf\x15\xc9Ly\xe9\xea\xed\xb4n|\x9f\x8c\xf2\x8b\x0c\xd3`\xabI\xb04\xb9\xb8\xed\xd6_\x1b\xb4\xb6V\x90\xae\\\xdaT\xe2\xc15\xe4=\xd2;!\x8e\x1c\xb0+l\xeb\xb2\x14\xcc\xb5\xa3b\x9c\xe6\xa2\x1e[\xe9s\xe43\x0f\xc1\xbd\x85\x0f\xc8\x01\xa8\x1dvV\xd0\xa1~\n\x1c\xad\x9f\xb2trF\xbd\xdeB\x87dv\x08\x94 \x02\x8d@\xfeb\x1ap;\x184b\x02EZ\xbfM\t\xcc\xcc\xf5\xd9t2\xb8s\xe4\x8d\xf6\xbc\x81,\xb8\xc8k\x99\x97\x08<\xf0\x8d\x0f: \x0f\xeb\xb79\xc3;\xd8\xd5N\x15nH\x13\xdf\xd4Q\xdaA@4-\xcf46\x06\x81\xc5\x0f\xb9Q\xa3X}"\xfb\xec\x1b\xc2\xfeG\xf4\xf4\xc8\xd3\xa4\xcd"\x8f\xde\x16e}\xda9\xb1F\xce\xb4>V\xcb\xfai\xb0\xde\xb2\x80\xfe\x1c\xdf\xcex\xe3Iw\xe7d\x9d\x9f%6\x7f\x7f\xdf\xad[\xd2].4\xe3\xb8eI\x02\x81\x81\x00\xb8\x07\xac|&;\xeb\x1a \x8d\xe8{b\tl%\xe1\x0b\x03\xd5}\xcd\x1c\xbb$\x08\x06\xf2a\'\xa0\xd6\xa4\x13\xe4\x92k\x05\xac\xe5yFd\nb\x96\xcbf\x8b\xe1\x84\t\xf8\xceu\x01\x0cA\xe7\x97~\xe0\xbe\x07J\x16BO\xf1\x1b\x9c\xd2U\xd9l#\xf0^\xb0T)\xd9\x95\xa7\x0b\xa8\xbf\xaeo\x19f\x0e\xf8\x94\xafAa\x88\xba\\\xa3\xf9\xb8|\xce,\xa3\xc9\x84\xbf\x1d2\x19C\xfa\x03\xd5[#\xdei\xc4\x91;\xcc\xe1\xa3\xcd\x02\x81\x81\x00\xec\x87\xc4\xc7\x1c\xd6\xfff~\xb6=\xab\xc3\xeam \xee6\xcf\xa9\xce\xe3O\xff"\xaf99\xd2X\x8d\x93Z\xf9\x08\x04\xdaK\x1a0\xa4\xc6\xa1\x06\xac]\x8e\xe1\xf0\xfdQ\xff\xfe\xef%o\x1d\xb6\tdkS\x00;\xb3\xa2of\xb4\xc0\xed\x8b\x92\xfeU\xb5\x86(\xfag\x83\x17\t\t\xc0*\xe3-\x0bC?i\xea\x01\xa6>\xbax\x1f\x1f\xb8U*\xbaO\x1cV_j\xa5\x14.\xf4\xce`K\xd6~A\xcb\xf8\xe4\x82\xcd\xe4+\x1b\x93\x02\x81\x80T\x1f}\xe3J~\xfd[v"(q\xae@\xecd\xecXb\xaaF\xd5j\x1a\xc9\xbf\xb9\x9d6x,\xf7\xb1\r>\xe1\x07w\x12\xaf\xdb\x1e(@\xef\x0cKrV\xe3\x01\xbe\xa53\x8b\x1c\xad\x83\xba\xdf\xef\xa9\xc0t\x08\x93\xe0@6\xd1\x0e\x80\xbf\xa9\xa1\xdbS\xd7\x94\xf7\x04"h\\q\xe1\xf3\xadC/\xf3\rH\xe8~\xac~oG\xf1m+\x8b\xff\xd1\'j\xbf\x85\xa4\xef-\xa5\x8b\x03P\x99I\x0e>oN\xe1\xac\xda]\x12\xc9\x02\x81\x80\x07[\xe6\x04g\xe2L\x89\xec\xd1P\xb3\xe2a\x8d\xc9\xa3\x7f\xb3\x10Nn\x86\x13\xa3\t\x9e\x97,\xf32\\nM\'1\xb7t\xf4\xb8\xa4\xb7\xc5T\xc6\xd2\x16Z\xf3;~l\x9f\x8a\xe38D\xcd`\x17n\xbbc[x(J\x9d\x00l\xac7VxqD7\x8bX\xd7\x15\x9e\x06\xda\xf5\xce\x9f\xc8\xcb\xfb\xe8\xa2+\xf4\xa7.vp\xbcO)V\x05\x01L\xea\xcd\xc9$1D\xa2}]Zc\xa1\xa5\xc5\xf8I\xa3\x1aj\xbby\x97\xdf\x02\x81\x81\x00\x8d\xfb\x94\xedI\xde"t\xbee\xbc\xe8\x8e\xb4,$I\xf4\xb5\x88Z\x1a\xd2\xbeV>\xe5P\xd8\xf8\x1a\x8e\xc3\x11d\xb6\x8f\xa4\xcd\xc4\x06\x19\x99c\xa2yg\x8a\xc0Iy%\xd2\xbdo\xc8\xd2\xa2\xa7dd\x81\xdaLl\x03\xdfY\x1aB\xb6\xfa*Y\xa5\xde$\xe6u\xb4\x81<K\xf0G\x06\x18F\x82\xa5\xaf\xbd\xe7\x82\x9b\xa4\xf13\x12\xc8\x80\xe1\xe7\xd89\xdc\xa4\x87\xcas\xac=\xef\xdb\xffu]\x8d\x7f\x0b\x9f\x10\xd5L\xbf\xa5\xc1@')
    token = b64decode(token)
    return b64encode(PRIVKEY.decrypt(token))

def register(s, url, login, password, isvip):
    r = s.get(url+'/signup/')
    resp = r.text
    promocode = id_generator(16)
    if isvip:
        promocode = getPromocode(resp).decode('utf-8')

    dataarr =  {'username':login,'password':password, 'promocode':promocode}
    r = s.post(url+'/signup/', data = dataarr)
    resp = r.text
    if 'User exists' in resp:
        quit(Status.CORRUPT, 'User exists error while registering')
    if not 'Kappa Bonus' in resp:
        quit(Status.CORRUPT, 'Buddy, your signup is f*cked up')


def auth(s, url, login, password, isget=False):
    r = s.get(url+'/login/')
    r = s.post(url+'/login/', data = {'username':login,'password':password})
    resp = r.text
    if 'Wrong login or password' in resp:
        if isget:
            quit(Status.CORRUPT, 'Can\'t login to get flag')
        else:
            quit(Status.MUMBLE, 'Can\'t login')

def put_flag(s, url, flag, team, cost, ischeck=False):
    r = s.post(url+'/sell/', data={'flag':flag,'team':str(team),'cost':str(cost)})
    if not flag in r.text:
        if ischeck:
            quit(Status.MUMBLE, 'Can\'t post flag')
        else:
            quit(Status.CORRUPT, 'Can\'t post flag')
    return re.findall(r'<td>(\d+)</td>', r.text)[0]

class Status(enum.Enum):
    OK      = 101
    CORRUPT = 102
    MUMBLE  = 103
    DOWN    = 104
    ERROR   = 110
    
    def __bool__(self):
        return self.value is Status.OK


__std_print = print

def print(*args, **kwargs):
    if "file" in kwargs:
        __std_print(*args, **kwargs)
    else:
        raise NameError("print() without file= should not be used")


def log(*args, **kwargs):
    if "file" in kwargs:
        raise NameError("use print() to print to file")
    
    __std_print(*args, **kwargs, file=sys.stderr)
    

def quit(code, *args, **kwargs):
    if "file" in kwargs:
        raise NameError("use print() to print to file")
    
    __std_print(*args, **kwargs)
    assert(type(code) == Status)
    sys.exit(code.value)


def check(host):
    # check if down with socket
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, int(PORT)))
        sock.send(b'GET / HTTP/1.1\n\n')
        sock.recv(20)
        sock.close()
    except:
        quit(Status.DOWN)
    
    s = requests.Session()
    url = 'http://'+host+':'+PORT
    login = id_generator(4) + '-' + id_generator(4) + '-' +id_generator(4)
    password = id_generator(16)
    isvip = False
    
    register(s, url, login, password, isvip)
    auth(s, url, login, password)

    # check status
    r = s.get(url+'/sell/')
    regexx = r': <b>(.*?)<\/b><\/p>'
    status = re.findall(regexx, r.text)[0]
    if isvip and status != 'VIP':
        quit(Status.MUMBLE, 'Checker can\'t get VIP')
    
    team = 1
    cost = random.randint(1,999)
    kappaflagid = put_flag(s, url, genflag(), team, cost, True)

    r = s.get(url+'/sell/')
    regexx = r': <b>(.*?)<\/b><\/p>'
    balance = re.findall(regexx, r.text)[1][1:]
    if balance != str(cost):
        quit(Status.CORRUPT, 'Bad balance after sell kappa')

    sl = requests.Session()
    login = id_generator(4) + '-' + id_generator(4) + '-' +id_generator(4)
    password = id_generator(16)
    isvip = False
    
    register(sl, url, login, password, isvip)
    auth(sl, url, login, password)

    # check status
    r = sl.get(url+'/sell/')
    regexx = r': <b>(.*?)<\/b><\/p>'
    status = re.findall(regexx, r.text)[0]
    if isvip and status != 'VIP':
        quit(Status.MUMBLE, 'Checker can\'t get VIP')
    
    team = 2
    lcbcflagid = put_flag(sl, url, genflag(), team, cost, True)

    r = sl.get(url+'/sell/')
    regexx = r': <b>(.*?)<\/b><\/p>'
    balance = re.findall(regexx, r.text)[1][1:]
    if balance != str(cost):
        quit(Status.CORRUPT, 'Bad balance after sell lcbc')

    rkappa = s.get(url+'/buyflag/'+kappaflagid)
    rlcbc = sl.get(url+'/buyflag/'+kappaflagid)
    if rkappa.text != rlcbc.text:
        log(rkappa.text, rlcbc.text)
        quit(Status.CORRUPT, 'can\'t buy flag')

    quit(Status.OK)


def put(host, flag_id, flag, vuln):
    s = requests.Session()
    url = 'http://'+host+':'+PORT
    login = flag_id
    password = id_generator(16)
    log(password)
    isvip = True
    register(s, url, login, password, isvip)
    auth(s, url, login, password)
    team = 0
    if vuln == '1':
        team = 1
    elif vuln == '2':
        team = 2
    
    cost = random.randint(10000,999999)
    flagid = put_flag(s, url, flag, team, cost)

    quit(Status.OK, login, password, sep=':')



def get(host, flag_id, flag, vuln):
    try:
        login, password = flag_id.split(":")
    except ValueError:
        quit(Status.CORRUPT, "I don't know password")
    
    s = requests.Session()
    url = 'http://'+host+':'+PORT
    r = s.get(url)
    share = 'X-Share-Flags' in r.headers

    auth(s, url, login, password, True)

    r = s.get(url+'/my')

    if not flag in r.text:
        quit(Status.CORRUPT, 'Can\'t get flag')    

    if share:
        quit(Status.OK, "Success: put flag", flag)
    else:
        quit(Status.OK)


def main():
    script, action, host, *args = sys.argv
    try:
        if action == "info":
            quit(Status.OK, "vulns:", VULNS)
        elif action == "check":
            check(host)
        elif action == "put":
            flag_id, flag, vuln = args
            put(host, flag_id, flag, vuln)
        elif action == "get":
            flag_id, flag, vuln = args
            get(host, flag_id, flag, vuln)
        else:
            log("Unknown action:", action)
            quit(Status.ERROR)
        
        log("Action handler has not quit correctly")
        quit(Status.ERROR)
    except SystemError as e:
        raise
    except Exception as e:
        traceback.print_exc()
        quit(Status.ERROR)


if __name__ == "__main__":
    main()
