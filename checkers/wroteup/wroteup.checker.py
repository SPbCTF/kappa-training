#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import enum

import requests
import string
import random
import re
import faker


VULNS = "1" # 1:2, 7:3, etc


class Status(enum.Enum):
    OK      = 101
    CORRUPT = 102
    MUMBLE  = 103
    DOWN    = 104
    ERROR   = 110
    
    def __bool__(self):
        return self.value is Status.OK

gen = faker.Factory().create()
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


def random_string(l = 10, charset = string.ascii_letters + string.digits):
    return ''.join(random.choice(charset) for _ in range(l))


def random_username():
    return random_string(4, string.ascii_lowercase + string.digits) + '-' + \
            random_string(4, string.ascii_lowercase + string.digits) + '-' + \
            random_string(4, string.ascii_lowercase + string.digits)

def check(host):
    try:
        sess = requests.Session()
        resp = sess.get("http://{}:50000/register".format(host))

        if resp.status_code != 200:
            log("[check] Get {} code".format(resp.status_code))
            quit(Status.MUMBLE, "Get {} code".format(resp.status_code))

        username = random_username()
        password = random_string()
        ctf = random_string()
        writeup = gen.text(random.randint(500, 2000))

        resp = sess.post("http://{}:50000/register".format(host), data={
            "login" : username,
            "password" : password
        })
        
        if resp.status_code != 200:
            log("[check] Can't register with username: {} and password: {}".format(username, password))
            quit(Status.MUMBLE, "Can't register")

        cookie = sess.cookies.get("KAPPA-AUTH")

        resp = sess.post("http://{}:50000/login".format(host), data={
            "login" : username,
            "password" : password
        })

        if resp.status_code != 200:
            log("[check] Can't log in with username: {} and password: {}".format(username, password))
            quit(Status.MUMBLE, "Can't log in")

        if cookie != sess.cookies.get("KAPPA-AUTH"):
            log("[check] Cookies after registration and login not equals")
            quit(Status.MUMBLE, "Cookies after registration and login not equals")

        resp = sess.post("http://{}:50000/post".format(host), data={
            "ctf" : ctf,
            "writeup" : writeup,
        })

        if resp.status_code != 200 or resp.text != "Success\n":
            log("[check] Post writeup handles {} code with {}".format(resp.status_code, resp.text))
            quit(Status.MUMBLE, "Post writeup handles {} code".format(resp.status_code))

        resp = sess.get("http://{}:50000/main".format(host))
        text = resp.text

        if ctf not in text or '@' + username not in text:
            log("Can't find ctf with name {} authored by {} on main page".format(ctf, username))
            quit(Status.MUMBLE, "Bad main page")
    
        resp = sess.get("http://{}:50000/show".format(host), params={
            "ctf" : ctf,
        })
        
        if writeup not in resp.text:
            log("Can't read own writeup")
            quit(Status.MUMBLE, "Can't read own writeup")

        username = random_username()
        password = random_string()
        resp = sess.post("http://{}:50000/register".format(host), data={
            "login" : username,
            "password" : password
        })

        resp = sess.get("http://{}:50000/show".format(host), params={
            "ctf" : ctf,
        }).text

        if len(resp) + 40 < len(writeup):
            log("Can't get encrypted writeup")
            quit(Status.MUMBLE, "Can't get previous writeup")

        quit(Status.OK)

    except requests.ConnectionError:
        quit(Status.DOWN, "Can't connect to service")
    except KeyError:
        quit(Status.MUMBLE, "Can't get cookie")


def put(host, flag_id, flag, vuln):
    try:
        username = random_username()
        password = random_string()
        writeup = gen.text(random.randint(500, 2000))

        sess = requests.Session()

        resp = sess.post("http://{}:50000/register".format(host), data={
            "login" : username,
            "password" : password
        })

        if resp.status_code != 200:
            log("[put] Can't register with username: {} and password: {}".format(username, password))
            quit(Status.MUMBLE, "Can't register")

        resp = sess.post("http://{}:50000/post".format(host), data={
            "ctf" : flag_id,
            "writeup" : writeup + flag,
        })

        if resp.status_code != 200 or resp.text != "Success\n":
            log("[put] Post writeup handles {} code with {}".format(resp.status_code, resp.text))
            quit(Status.MUMBLE, "Can't post writeup")

        quit(Status.OK, "{}:{}:{}".format(username, password, flag_id))

    except requests.ConnectionError:
        quit(Status.DOWN, "Can't connect to service")


def get(host, flag_id, flag, vuln):
    try:
        username, password, flag_id = flag_id.split(':')
        
        sess = requests.Session()

        resp = sess.post("http://{}:50000/login".format(host), data={
            "login" : username,
            "password" : password
        })

        if resp.status_code != 200:
            log("[get] Can't log in with username: {} and password: {}".format(username, password))
            quit(Status.CORRUPT, "Can't log in")

        resp = sess.get("http://{}:50000/show".format(host), params={
            "ctf" : flag_id,
        })

        if flag not in resp.text:
            log("Can't find flag on show page")
            quit(Status.CORRUPT, "Can't get flag")

        quit(Status.OK)

    except requests.ConnectionError:
        quit(Status.DOWN, "Can't connect to service")


def main():
    action, *args = sys.argv[1:]
    try:
        if action == "info":
            quit(Status.OK, "vulns:", VULNS)
        elif action == "check":
            host, = args
            check(host)
        elif action == "put":
            host, flag_id, flag, vuln = args
            put(host, flag_id, flag, vuln)
        elif action == "get":
            host, flag_id, flag, vuln = args
            get(host, flag_id, flag, vuln)
        else:
            log("Unknown action:", action)
            quit(Status.ERROR)
        
        log("Action handler has not quit correctly")
        quit(Status.ERROR)
    except SystemError as e:
        raise
    except Exception as e:
#        traceback.print_exc()
        quit(Status.ERROR)


if __name__ == "__main__":
    main()
