#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

argvv = [] + sys.argv

import enum
from pwn import *
from faker import Faker
from faker.providers import internet
import random
import string
import os

VULNS = "1:1" # 1:2, 7:3, etc
PORT = "7878"

fake = Faker()
fake.add_provider(internet)

def id_generator(size=8, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))

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
    try:
        username = fake.domain_word() + str(random.randint(1,31337))
        password = id_generator()
        token = ''
        review = fake.sentence(10)

        sock = remote(host, PORT, level=60)

        # register
        sock.recvuntil('\n\n')
        sock.send('1\n')

        # send username
        sock.recvuntil('\n')
        sock.send(username+'\n')

        # send password
        sock.recvuntil('\n')
        sock.send(password+'\n')

        # check money and send token
        resp = sock.recvuntil('Quit\n\n').decode("utf-8")
        money, token, *trash = resp.split('\n')
        if 'money' not in money:
            quit(Status.MUMBLE, 'No \'money\' in output')
        token = token.split(' ')[3]
        if not token:
            quit(Status.MUMBLE, 'Token is empty')

        # check user list
        sock.send('3\n')
        userlist = sock.recvuntil('\n\n').decode("utf-8")
        if not username in userlist:
            quit(Status.MUMBLE, 'New user not found in the list')

        # buy random thing
        sock.send('2\n')

        spinners = sock.recvuntil('\n\n').decode("utf-8")
        if not 'Caviar Spinner Tricolor: 1000$' in spinners:
            quit(Status.MUMBLE, 'Caviar spinner is not default')
        if not 'iPhone Fidget Spinner: 500$' in spinners:
            quit(Status.MUMBLE, 'iPhone spinner is not default')
        if not 'Atesson Fidget Spinner: 20$' in spinners:
            quit(Status.MUMBLE, 'Atesson spinner is not default')

        vapes = sock.recvuntil('\n\n').decode("utf-8")
        if not 'Athea Mods Gimmick: 1000$' in vapes:
            quit(Status.MUMBLE, 'Athea vape is not default')
        if not 'Predator Cap S: 500$' in vapes:
            quit(Status.MUMBLE, 'Predator vape is not default')
        if not 'Monster Vapor Vapex: 100$' in vapes:
            quit(Status.MUMBLE, 'Monster vape is not default')
        # buy random item
        choice = str(random.randint(1,6))

        sock.recvuntil(':')
        sock.recvuntil(':')
        sock.recvuntil('\n')
        sock.send(choice + '\n')

        sock.recvuntil('\n')
        succ = sock.recvuntil('\n').decode("utf-8")
        if not 'Success' in succ:
            quit(Status.MUMBLE, 'Can\'t buy item with number ', choice)
        sock.recvuntil('\n')
        sock.recvuntil('\n')
        sock.recvuntil('\n')
        sock.recvuntil('\n')
        sock.recvuntil('\n')

        #send review
        sock.send(review+'\n')
        sock.recvuntil('\n\n')
        sock.recvuntil('\n\n')

        # quit from shop
        sock.send('8'+'\n')

        # check if item was really bought
        sock.recvuntil('\n\n')
        sock.send('5'+'\n')
        my_items = sock.recvuntil('\n\n').decode("utf-8")
        if not review.replace(' ', '_') in my_items:
            quit(Status.MUMBLE, 'Bought item was not found ', choice)

        # check auth with generated token
        sock.recvuntil('\n\n')
        sock.send('4'+'\n')
        sock.recvuntil('\n')
        sock.send(token+'\n')
        resp = sock.recvuntil('\n').decode("utf-8")
        if 'token not found' in resp:
            quit(Status.MUMBLE, 'Can\'t authorize with given token')
        quit(Status.OK)
    #except EOFError:
    #    quit(Status.DOWN, 'EOFError while recv smth')
    except PwnlibException as e:
        quit(Status.DOWN, 'Failed to connect')

def put(host, flag_id, flag, vuln):
    try:
        username = flag_id
        password = id_generator()
        token = ''
        review = flag

        sock = remote(host, PORT, level=60)
        # register
        sock.recvuntil('\n\n')
        sock.send('1\n')
        
        # send username
        sock.recvuntil('\n')
        sock.send(username+'\n')

        # send password
        sock.recvuntil('\n')
        sock.send(password+'\n')

        money, token, *trash = sock.recvuntil('\n\n').decode("utf-8").split('\n')
        token = token.split(' ')[3]
        sock.recvuntil('\n\n')
        sock.send('2\n')

        spinners = sock.recvuntil('\n\n').decode("utf-8")
        vapes = sock.recvuntil('\n\n').decode("utf-8")
        choice = ''
        if vuln == '1':
            choice = random.randint(1,3)
        elif vuln == '2':
            choice = random.randint(4,6)
        
        sock.recvuntil(':')
        sock.recvuntil(':')
        sock.recvuntil('\n')
        sock.send(str(choice) + '\n')

        sock.recvuntil('\n')
        succ = sock.recvuntil('\n').decode("utf-8")
        if not 'Success' in succ:
            quit(Status.MUMBLE, 'Can\'t buy item with number ', choice)
        sock.recvuntil('\n')
        sock.recvuntil('\n')
        sock.recvuntil('\n')
        sock.recvuntil('\n')
        sock.recvuntil('\n')

        #send review
        sock.send(review+'\n')
        sock.recvuntil('\n\n')
        sock.recvuntil('\n\n')
        
        # quit from shop
        sock.send('8'+'\n')

        # check if item was really bought
        sock.recvuntil('\n\n')
        sock.send('5'+'\n')
        my_items = sock.recvuntil('\n\n').decode("utf-8")
        if not review.replace(' ', '_') in my_items:
            quit(Status.MUMBLE, 'Bought item was not found ', choice)

        # quit
        sock.recvuntil('\n\n')
        sock.send('6'+'\n')

        quit(Status.OK, username, token, sep=':')
    except PwnlibException as e:
        quit(Status.DOWN, 'Failed to connect')
    except EOFError:
        quit(Status.DOWN, 'Failed to recv smth')

def get(host, flag_id, flag, vuln):
    try:
        try:
            username, token = flag_id.split(":")
        except ValueError:
            quit(Status.CORRUPT, "I don't know token")
        
        sock = remote(host, PORT, level=60)
        
        sock.recvuntil('\n\n')
        try:
            sock.send('4'+'\n')
            sock.recvuntil('\n')
            sock.send(token+'\n')
            resp = sock.recvuntil('\n').decode("utf-8")
        except EOFError as e:
            quit(Status.CORRUPT, 'Can\'t authorize')

        if 'token not found' in resp:
            quit(Status.CORRUPT, 'Can\'t authorize')
        sock.recvuntil('\n\n')

        sock.send('5'+'\n')
        my_items = sock.recvuntil('\n\n').decode("utf-8")
        if not flag.replace(' ', '_') in my_items:
            quit(Status.CORRUPT, 'Can\'t get flag')

        quit(Status.OK)
    except PwnlibException as e:
        quit(Status.DOWN, 'Failed to connect')
    except EOFError:
        quit(Status.DOWN, 'Failed to recv smth')

def main():
    self_file, action, *args = argvv
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
        traceback.print_exc()
        quit(Status.ERROR)


if __name__ == "__main__":
    main()
