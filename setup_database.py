# -*- coding:utf-8 -*-

import sqlite3

conn = sqlite3.connect('Book_DB.sqlite3')
cursor = conn.cursor()
sql_cmd = 'create table book(isbn interger primary key, title text, title_key text,author text, author_key text, publisher text, label text,day int, pages int, thumbnail text)'
cursor.execute(sql_cmd)
conn.commit()

conn.close()