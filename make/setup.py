import sqlite3

conn = sqlite3.connect('ln.db')
c = conn.cursor()

c.execute('CREATE TABLE options  (name text primary key, val text)')
c.execute('CREATE TABLE servers  (id integer primary key, name text, username text, password text)')
c.execute('CREATE TABLE groups   (id integer primary key, server_id integer, name text, cache integer, count integer, first integer, last integer)')
c.execute('CREATE TABLE articles (id integer primary key, server_id integer, group_id integer, title text, body text)')
conn.commit()
conn.close()


