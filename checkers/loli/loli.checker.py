#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import enum

import requests
import string
import random
import re


VULNS = "1" # 1:2, 7:3, etc


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


def random_string(l = 10, charset = string.ascii_letters + string.digits):
    return ''.join(random.choice(charset) for _ in range(l))


def random_username():
    return random_string(4, string.ascii_lowercase + string.digits) + '-' + \
            random_string(4, string.ascii_lowercase + string.digits) + '-' + \
            random_string(4, string.ascii_lowercase + string.digits)

def check(host):
    try:
        resp = requests.get("http://{}:4242/main".format(host))
        text = resp.text

        if resp.status_code == 451:
            log("RKN BAN, Yahoo")
            quit(Status.MUMBLE, "RKN banned you")

        if resp.text == "You will be unbanned":
            log("RKN unban")
            quit(Status.MUMBLE, "Request to unban")

        if "KappaProtect" not in text:
            log("Not found \"KappaProtect\"")
            quit(Status.MUMBLE, "Bad main page")

        quiz = random_username()
        ids = ','.join([random_string() for _ in range(5)])
        answer = random_string(5, 'yn')
        flag = random_string(32, string.ascii_lowercase)

        resp = requests.get("http://{}:4242/createquiz".format(host), params={
            "name" : quiz,
            "ids" : ids,
            "answer" : answer,
            "flag" : flag,
        })

        if resp.status_code == 451:
            log("RKN BAN, Yahoo")
            quit(Status.MUMBLE, "RKN banned you")

        if resp.text == "You will be unbanned":
            log("RKN unban")
            quit(Status.MUMBLE, "Request to unban")

        text = resp.text
        code = resp.status_code // 100

        if code == 4:
            log("[createquiz] return {} code to params:\n\tname: {}\n\tids: \
                {}\n\tanswer: {}\n\tflag: {}\n".format(resp.status_code, quiz, ids, answer, flag))
            quit(Status.MUMBLE, "Get {} code from createquiz".format(resp.status_code))
        
        if code == 5:
            log("[createquiz] return {} code to params:\n\tname: {}\n\tids: \
                {}\n\tanswer: {}\n\tflag: {}\n".format(resp.status_code, quiz, ids, answer, flag))
            quit(Status.DOWN, "Get {} code from createquiz".format(resp.status_code))

        if text != 'Nya!':
            log("[createquiz] Not found 'Nya!' in answer")
            quit(Status.MUMBLE, "Bad answer from service")

        resp = requests.get("http://{}:4242/main".format(host))

        if resp.status_code == 451:
            log("RKN BAN, Yahoo")
            quit(Status.MUMBLE, "RKN banned you")

        if resp.text == "You will unbanned":
            log("RKN unban")
            quit(Status.MUMBLE, "Request to unban")

        text = resp.text

        if quiz not in text:
            log("[main] Can't get name of previos quiz")
            quit(Status.MUMBLE, "Can't see quiz list")

        if re.search("<th.*>{}</th><td.*>(5)</td>".format(quiz), text) is None:
            log("[main] Can't get count of pictures in quiz")
            quit(Status.MUMBLE, "Can't see pictures count in quiz")

        resp = requests.get("http://{}:4242/quiz".format(host), params={
            "name" : quiz,
        })
        text = resp.text
        code = resp.status_code // 100

        if resp.status_code == 451:
            log("RKN BAN, Yahoo")
            quit(Status.MUMBLE, "RKN banned you")

        if resp.text == "You will unbanned":
            log("RKN unban")
            quit(Status.MUMBLE, "Request to unban")

        if code == 4:
            log("[quiz] return {} code to params:\n\tname: {}\n\tids: \
                {}\n\tanswer: {}\n\tflag: {}\n".format(resp.status_code, quiz, ids, answer, flag))
            quit(Status.MUMBLE, "Get {} code from quiz".format(resp.status_code))
        
        if code == 5:
            log("[quiz] return {} code to params:\n\tname: {}\n\tids: \
                {}\n\tanswer: {}\n\tflag: {}\n".format(resp.status_code, quiz, ids, answer, flag))
            quit(Status.DOWN, "Get {} code from quiz".format(resp.status_code))

        for picture in ids.split(','):
            if picture not in text:
                log("[quiz] Can't find picture with {} id".format(picture))
                quit(Status.MUMBLE, "Can't see picture id")

        
        resp = requests.get("http://{}:4242/postquiz".format(host), params={
            "name" : quiz,
            "answer" : answer,
        })
        text = resp.text
        code = resp.status_code // 100

        if resp.status_code == 451:
            log("RKN BAN, Yahoo")
            quit(Status.MUMBLE, "RKN banned you")

        if resp.text == "You will unbanned":
            log("RKN unban")
            quit(Status.MUMBLE, "Request to unban")

        if code == 4:
            log("[postquiz] return {} code to params:\n\tname: {}\n\tids: \
                {}\n\tanswer: {}\n\tflag: {}\n".format(resp.status_code, quiz, ids, answer, flag))
            quit(Status.MUMBLE, "Get {} code from postquiz".format(resp.status_code))
        
        if code == 5:
            log("[postquiz] return {} code to params:\n\tname: {}\n\tids: \
                {}\n\tanswer: {}\n\tflag: {}\n".format(resp.status_code, quiz, ids, answer, flag))
            quit(Status.DOWN, "Get {} code from postquiz".format(resp.status_code))

        if text != flag:
            log("[postquiz] Flags {} and {} are not equal".format(text, flag))
            quit(Status.MUMBLE, "Flags are not equal")

        order = [i for i in range(0, 5)]
        random.shuffle(order)
        new_answer = ''.join([answer[order[i]] for i in range(0, 5)])
        order = ','.join([str(i) for i in order])

        resp = requests.get("http://{}:4242/postquiz".format(host), params={
            "name" : quiz,
            "answer" : new_answer,
            "order" : order,
        })
        text = resp.text
        code = resp.status_code // 100

        if resp.status_code == 451:
            log("RKN BAN, Yahoo")
            quit(Status.MUMBLE, "RKN banned you")

        if resp.text == "You will unbanned":
            log("RKN unban")
            quit(Status.MUMBLE, "Request to unban")

        if code == 4:
            log("[postquiz] return {} code to params:\n\tname: {}\n\tids: \
                {}\n\tanswer: {}\n\tflag: {}\n".format(resp.status_code, quiz, ids, answer, flag))
            quit(Status.MUMBLE, "Get {} code from postquiz".format(resp.status_code))
        
        if code == 5:
            log("[postquiz] return {} code to params:\n\tname: {}\n\tids: \
                {}\n\tanswer: {}\n\tflag: {}\n".format(resp.status_code, quiz, ids, answer, flag))
            quit(Status.DOWN, "Get {} code from postquiz".format(resp.status_code))

        quit(Status.OK)

    except requests.ConnectionError:
        quit(Status.DOWN, "Can't connect to service")


def put(host, flag_id, flag, vuln):
    try:
        ids = ','.join([random_string() for _ in range(30)])
        answer = random_string(30, 'yn')

        resp = requests.get("http://{}:4242/createquiz".format(host), params={
            "name" : flag_id,
            "ids" : ids,
            "answer" : answer,
            "flag": flag,
        })

        text = resp.text
        code = resp.status_code // 100

        if resp.status_code == 451:
            log("RKN BAN, Yahoo")
            quit(Status.MUMBLE, "RKN banned you")

        if resp.text == "You will unbanned":
            log("RKN unban")
            quit(Status.MUMBLE, "Request to unban")

        if code == 4:
            log("[put|createquiz] return {} code to params:\n\tname: {}\n\tids: \
                {}\n\tanswer: {}\n\tflag: {}\n".format(resp.status_code, flag_id, ids, answer, flag))
            quit(Status.MUMBLE, "Get {} code from createquiz".format(resp.status_code))
        
        if code == 5:
            log("[put|createquiz] return {} code to params:\n\tname: {}\n\tids: \
                {}\n\tanswer: {}\n\tflag: {}\n".format(resp.status_code, flag_id, ids, answer, flag))
            quit(Status.DOWN, "Get {} code from createquiz".format(resp.status_code))

        if text != 'Nya!':
            log("[put|createquiz] Not found 'Nya!' in answer")
            quit(Status.MUMBLE, "Bad answer from service")

        quit(Status.OK, "{}:{}".format(flag_id, answer))

    except requests.ConnectionError:
        quit(Status.DOWN, "Can't connect to service")


def get(host, flag_id, flag, vuln):
    try:
        quiz, answer = flag_id.split(':')
        order = [i for i in range(0, 30)]
        random.shuffle(order)
        new_answer = ''.join([answer[order[i]] for i in range(0, 30)])
        order = ','.join([str(i) for i in order])

        resp = requests.get("http://{}:4242/postquiz".format(host), params={
            "name" : quiz,
            "answer" : answer,
#            "answer" : new_answer,
#            "order": order,
        })

        if resp.status_code == 451:
            log("RKN BAN, Yahoo")
            quit(Status.MUMBLE, "RKN banned you")

        if resp.text == "You will unbanned":
            log("RKN unban")
            quit(Status.MUMBLE, "Request to unban")

        if resp.status_code == 400:
            log("Quiz not found")
            quit(Status.CORRUPT, "Quiz not found")

        text = resp.text
        code = resp.status_code // 100

        if code == 4:
            log("[get|postquiz] return {} code to params:\n\tname: {}\n\torder: \
                {}\n\tanswer: {}\n".format(resp.status_code, flag_id, order, new_answer))
            quit(Status.MUMBLE, "Get {} code from postquiz".format(resp.status_code))
        
        if code == 5:
            log("[get|postquiz] return {} code to params:\n\tname: {}\n\torder: \
                {}\n\tanswer: {}\n".format(resp.status_code, flag_id, order, new_answer))
            quit(Status.DOWN, "Get {} code from postquiz".format(resp.status_code))

        if flag != text:
            quit(Status.CORRUPT, "Unknown flag")

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
